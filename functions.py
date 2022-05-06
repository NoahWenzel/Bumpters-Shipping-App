import urllib.request
from PyPDF4 import PdfFileReader, PdfFileWriter
import subprocess

def parseAddress(address):
    temp = address.split('\n')
    if len(temp) == 3:
        name = temp[0][:-1]
        street1 = temp[1][:-1]
        street2 = None
        temp = temp[2].split(',')
        city = temp[0]
        temp = temp[1].split()
        state = temp[0]
        zip = temp[1]
    else:
        name = temp[0][:-1]
        street1 = temp[1][:-1]
        street2 = temp[2][:-1]
        temp = temp[3].split(',')
        city = temp[0]
        temp = temp[1].split()
        state = temp[0]
        zip = temp[1]

    return {
        "name": name,
        "street1": street1,
        "street2": street2,
        "city": city,
        "state": state,
        "zip": zip,
        "country": "US"
    }


def download_pdf_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()


def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)


def download_labels(purchased_url_list):
    downloaded_labels = []
    file_path = "./labels/"

    for i in range(len(purchased_url_list)):
        download_pdf_file(purchased_url_list[i], "labels/label_" + str(i))
        downloaded_labels.append(file_path + "label_" + str(i) + ".pdf")

    merge_pdfs(downloaded_labels,
                "./labels/EndResult.pdf")

    # os.startfile("labels\EndResult.pdf") <--- This line worked on windows but doesn't appear to work on mac
    subprocess.call(['open', 'labels/EndResult.pdf'])

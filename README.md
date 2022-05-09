# Bumpters-Shipping-App

This application was designed specifically for the company Bungsters Brix. This is a basic application that can create multiple USPS shipments with the same senders address.

# User's guide

<h2>Step 1: Login</h2>
You will first be presented with a login page that will ask for a name and API Key. 

The name field will be your username and will be associated with all information (`from_address` & `carrier_account` id). If the name entered already has a user associated with it then the `from_address` and `carrier_account`, if already entered, with automatically be populated on the user's page and will be used when creating shipments.

The API Key field needs to be a valid EasyPost API Key. This will be validated upon login and cannot be a dummy key or have any mistakes. If you need to create or view your EasyPost API Key you can do so [here](https://www.easypost.com/account/api-keys).


<h2>Step 2: Account Info</h2>
If you are using the app for the first time you will need to go to the user page to enter in your `from_address.id` and `carrier_account.id`.

The `from_address.id` will need to be created in advance using the EasyPost API. I have linked the EasyPost documentation on how to do this [here](https://www.easypost.com/docs/api/python#addresses).

The `carrier_account.id` can be found on your EasyPost [Carrier Account Dashboard](https://www.easypost.com/account/carriers).

Once you have entered the `from_address.id` and the `carrier_account.id` they will be saved and associated with the name you entered on loging in so you will not have to enter them after logging in next time.

<h2>Step 3: Create a Shipment</h2>
On the shipments page you will be able to create a new shipment by entering in the requested information. The address is designed to be coppied in from FaceBook Marketplace once a sale is made and is formatted as follows:

```
FirstName LastName
Street1
Street2
City, State(2Letter) zipcode

Example:
John Doe
123 Sesame Street
Suite 101
New York, NY 12345
```
Note that if street2 is not available the line may be omitted entirely.

You will also be able to remove shipments when viewing them from the batch page. All you have to do is click the button below the shipment that says "Remove shp_xxxxxxxxxxxxxx". As you can see the shipment ID will also be on the button for clarification and accuracy.

<h2>Step 4: Purchase The Batch</h2>
Once you have added all shipments that you want and are ready to purchase them you can head on over to the batch page to view all shipments and their detials. Once satisfied you may click the button at the bottom of the page "Purchase Batch!".

Clicking on this button will start the process of purchasing the batch. Please be aware that depending on how large the batch is this may take a while. Once the entire batch is purchased a new page will open up that contains the PDF labels ready for you to print. Note that you will also be logged out once the batch has been purchased.



<h1>Warning!!!</h1>
This code was written for a specific company and only intended to be used by one particular user. Eventually this may be a hosted publicly available app. Because of this unique situation there are strange design and security choices. Most of them are only placeholders so that I can improve upon the security and design of this application at a later point in time. Do not make this project publicly available as this could pose a serious security risk.

This app is still very much a work in progress, it's basic skeleton works but it is in need of major cosmetic and security work to make this safe to be used by others anyone.
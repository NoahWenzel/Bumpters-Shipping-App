from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import easypost
import functions

app = Flask(__name__)
app.secret_key = 'anystringhere84651'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=90)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    from_address_id = db.Column(db.String(100))
    carrier_account_id_USPS = db.Column(db.String(100))

    def __init__(self, name, from_address_id, carrier_account_id_USPS):
        self.name = name
        self.from_address_id = from_address_id
        self.carrier_account_id_USPS = carrier_account_id_USPS

@app.route('/home/', methods=['POST', 'GET'])
@app.route('/shipment/', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        easypost.api_key = session['api_key']

        length = float(request.form['length'])
        width = float(request.form['width'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        to_address = request.form['address']

        user = session['user']
        user = users.query.filter_by(name=user).first()
        try:
            from_address = easypost.Address.retrieve(str(user.from_address_id))
        except:
            flash('From address ID is invalid, please correct!', 'info')
            return redirect(url_for('user'))

        try:
            to_address = functions.parseAddress(to_address)
        except:
            flash('To address incorrectly formatted, please retry!', 'info')
            return redirect(url_for('home'))

        try:
            to_address = easypost.Address.create(
                name=to_address['name'],
                street1=to_address['street1'],
                street2=to_address['street2'],
                city=to_address['city'],
                state=to_address['state'],
                zip=to_address['zip'],
                country=to_address['country'],
            )
        except:
            flash('To Address is invalid, please try again!', 'info')
            return redirect(url_for('home'))

        try:
            parcel = easypost.Parcel.create(
                length=length,
                width=width,
                height=height,
                weight=weight,
            )
        except:
            flash('Parcel dimensions are invalid, please try again!', 'info')
            return redirect(url_for('home'))

        try:
            shipment = easypost.Shipment.create(
                reference='Ref',
                from_address=from_address,
                to_address=to_address,
                parcel=parcel,
                # Note that this can only rate against one carrier account at a time right now (in this case USPS)
                    # In the future I could expand this.
                carrier_accounts=user.carrier_account_id_USPS,
                options={
                    'label_format': 'PDF',
                    'label_size': '4x6',
                }
            )
        except easypost.Error as e:
            e.json_body['message']
            e.json_body['code']
            flash('Something went wrong.......', 'info')
            return redirect(url_for('home'))

        # Add the shipment to the batch
        batch.add_shipments(shipments=[
            {'id': shipment.id}
        ])

        flash(f'Shipment {shipment.id} created and added successfully!', 'info')
        flash(f'Batch_ID: {batch.id}', 'info')
        return redirect(url_for('home'))

        # TODO: CREATE OPTIONAL MANIFEST
        # Have a button at the bottom of the page to review and purchase batch.
        # Send them to a new page that has all the shipments on the page

    else:
        if 'user' in session:
            user = session['user']
            return render_template('home.html', user = user)
        else:
            return redirect(url_for('login'))


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        api_key = request.form['api_key']
        session['user'] = user
        session['api_key'] = api_key

        # Every time they login validate their EP API key by creating a batch
        try:
            easypost.api_key = api_key
            global batch
            batch = easypost.Batch.create()
        except:
            flash('API Key was invalid, please try again!', 'info')
            return redirect(url_for('logout'))

        found_user = users.query.filter_by(name=user).first()

        if found_user:
            session['from_address_id'] = found_user.from_address_id
            #TODO: I should really find a way to validate this carrier account ID on login even in test before using it
                # I'll worry about this later though it's low priority at the moment as this is only designed to be used by one person
            session['carrier_account_id_USPS'] = found_user.carrier_account_id_USPS
            
        else:
            # Add new user if they don't already exist
            session['from_address_id'] = ''
            session['carrier_account_id_USPS'] = ''
            db.session.add(users(user, '', ''))
            db.session.commit()
            return redirect(url_for('user'))
            
        return redirect(url_for('home'))
    else:
        if 'user' in session:
            return redirect(url_for('home'))
        return render_template('login.html')


@app.route('/logout/')
def logout():
    if 'user' in session:
        user = session['user']
        flash(f'{user} has been Logged out!', 'info')

    session.pop('user', None)
    session.pop('api_key',  None)
    session.pop('from_address_id',  None)
    session.pop('carrier_account_id_USPS', None)
    return redirect(url_for('login'))


#TODO: Make it so that you can change the from_address_ID by entering in an address
    # Maybe validate further with part of the API key to make sure that the address ID is shown to the correct user
    # I could also make it so that this address ID is not seen or changed directly but rather save the entire address
        # and have the ID hidden to the user... but that would mean displaying the address which I would like to avoid
@app.route('/user/', methods=['POST', 'GET'])
def user():
    from_address_id = None
    carrier_account_id_USPS = None
    if 'user' in session:
        user = session['user']

        if request.method == 'POST':
            from_address_id = request.form['from_address_id']
            carrier_account_id_USPS = request.form['carrier_account_id_USPS']
            session['from_address_id'] = from_address_id
            session['carrier_account_id_USPS'] = carrier_account_id_USPS
            found_user = users.query.filter_by(name=user).first()
            found_user.from_address_id = from_address_id
            found_user.carrier_account_id_USPS = carrier_account_id_USPS
            db.session.commit()
            flash('Address ID and Carrier Account ID has been saved!!!')

        return render_template('user.html', from_address_id=session['from_address_id'], carrier_account_id_USPS=session['carrier_account_id_USPS'])
    else:
        return redirect(url_for('login'))


# TODO: include a checkbox for whether or not you want the shipments manifested.
@app.route('/batch/', methods=['POST', 'GET'])
def batch():
    easypost.api_keys = session['api_key']

    if request.method == 'POST':
        # Remove shipment from the batch!
        if request.form['action'] != 'Purchase Batch!':
            rm_shp = request.form['action'].split()
            rm_shp = rm_shp[1]

            batch.remove_shipments(
                shipments=[
                    {'id': rm_shp}
                ]
            )

            flash(f'{rm_shp} was removed', 'info')
            # Just continue on showing the batch page after the shipment was removed


        if request.form['action'] == 'Purchase Batch!':
            # Purchase batch!
            # Unfortunately, I will have to iterate through the batch and buy each shipment individually 
                # because I want the lowest rate available per shipment and don't want to rely on providing 
                # a service to user the batch.buy() function...
            for shp in batch.shipments:
                current_shipment = easypost.Shipment.retrieve(shp.id)
                current_shipment.buy(rate=current_shipment.lowest_rate())

            # Now find the shipping labels and open them up in a new window
            # Extract label URL's from shipments in batch
            purchased_url_list = []

            for shp in batch.shipments:
                current_shipment = easypost.Shipment.retrieve(shp.id)
                purchased_url_list.append(current_shipment.postage_label.label_url)
            
            functions.download_labels(purchased_url_list)

            flash(f"Batch {batch.id} was purchased successfully!!!", 'info')
            return redirect(url_for('logout'))


    # Now I can just view the shipments in the batch
    shipments_info = []
    for shp in batch.shipments:
        current_shipment = easypost.Shipment.retrieve(shp.id)
        shipments_info.append(
            {
                'shp_id': current_shipment.id,
                'to_address': current_shipment.to_address,
                'parcel': current_shipment.parcel,
            }
        )

    return render_template('batch.html', batch_id=batch.id, shipments_info=shipments_info)
    

# This is temporary to give me visibility into what's going on in the database momentarily
@app.route('/view/')
def view():
    return render_template('view.html', values=users.query.all())  



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, redirect, request, session, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # This is the import you need
import re, hashlib
from source.databaseConnection import Database
import os
import pandas as pd 
import csv
from source.userInputNeuralNetwork import predict
#from source.userInputGradientBoosting import predict

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://tkagande:@127.0.0.1/irental'
)

app = Flask(__name__, template_folder='./public')


# Configure the SQLAlchemy part of the app
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Database and Migration Setup ---flask checkdb

# 1. Initialize the SQLAlchemy db object
db = SQLAlchemy(app)

# 2. Initialize the Flask-Migrate object
#    This connects the Flask app and the SQLAlchemy database
#    to the migration capabilities.
migrate = Migrate(app, db)

@app.cli.command("checkdb")
def check_db_connection():
    """Checks if the database connection is valid."""
    try:
        # db.engine is the low-level SQLAlchemy engine
        with db.engine.connect() as connection:
            # Try to execute a simple query
            connection.execute(db.text("SELECT 1"))
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed:")
        print(f"\n{e}")

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(35), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    
    def __repr__(self):
        return f'<User {self.email}>'

class Suburb(db.Model):
    __tablename__ = 'suburbs'

    id = db.Column(db.Integer, primary_key=True)
    constituency = db.Column(db.String(35), nullable=False)
    council = db.Column(db.String(35), nullable=False)
    suburb = db.Column(db.String(45), nullable=False, unique=True)
    density = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self):
        return f'<Suburb {self.suburb}>'

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(35), nullable=False)
    price = db.Column(db.Numeric(16, 2), nullable=False) # Numeric is correct for money
    suburb = db.Column(db.String(35), nullable=False)
    property = db.Column(db.String(35), nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    bedroom = db.Column(db.Integer, nullable=False)
    toilets = db.Column(db.Integer, nullable=False)
    ensuite = db.Column(db.Integer, nullable=False)
    condi = db.Column(db.Integer, nullable=False)
    carport = db.Column(db.Integer, nullable=False)
    pool = db.Column(db.Boolean, nullable=False)
    furnished = db.Column(db.Boolean, nullable=False)
    cottage = db.Column(db.Integer, nullable=False)
    power = db.Column(db.Boolean, nullable=False)
    pbackup = db.Column(db.Boolean, nullable=False)
    water = db.Column(db.Boolean, nullable=False)
    wbackup = db.Column(db.Boolean, nullable=False)
    gated = db.Column(db.Boolean, nullable=False)
    garden = db.Column(db.Boolean, nullable=False)
    address = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(130), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # --- Note on Foreign Keys ---
    # Your schema uses plain strings for 'email' and 'suburb'.
    # For a more robust (relational) database, you would replace these
    # with Foreign Keys pointing to the User and Suburb tables, e.g.:
    #
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # suburb_id = db.Column(db.Integer, db.ForeignKey('suburbs.id'), nullable=False)
    #
    # But I have translated your schema exactly as you provided it.

    def __repr__(self):
        return f'<Property {self.address}>'

# enable debugging mode
#app.config["DEBUG"] = True
app.config['TESTING'] = True
# Upload folder
app.config['UPLOAD_FOLDER'] =  'static/uploads'

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Database Connection
connection = Database(host="127.0.0.1", user="tkagande", password="", dbname="irental")
connection.connect()

@app.route('/', methods=['GET'])
def index():
    properties =  connection.posts("SELECT * FROM properties")
    return render_template('/index.html', properties = properties)

@app.route("/predication")
def predication():
    return send_file(
        "./static/downloads/predication-price-template.zip",
        mimetype="application/zip",
        download_name="predication-price-template.zip",
        as_attachment=True,) 

@app.route('/price', methods=['GET', 'POST'])
def pricepredication():
    if (request.method == "POST"):
        file = request.files['file']
        try:
            input = pd.read_csv(file)
            print(input.iloc[0, 0])
            suburb = input.iloc[0, 0]
            record = connection.post("SELECT * FROM suburbs WHERE suburb = '{}'".format(suburb))
            print(record)
            if record != None:
                input.insert(10, 'council', record[1], True)
                input.insert(9, 'constituency', record[2], True)
                input.insert(1, 'density', record[4], True)     
                print(record)   
                print(input.tail())
                output = predict.userInput(input)
                return render_template('rental/output.html', price = output)
            else:
                flash("Suburb not found")
                return render_template('rental/price.html') 
        except Exception as e:
            flash("An error occurred:", e)
            return render_template('rental/price.html')
    else:
        return render_template('rental/price.html')
               
@app.route("/property")
def property():
    return send_file(
        "./static/downloads/properties-upload-template.zip",
        mimetype="application/zip",
        download_name="properties-upload-template.zip",
        as_attachment=True,) 
    
@app.route('/properties', methods=['GET', 'POST'])
def properties():
    if (request.method == "POST"):
        file = request.files['properties']
        if file.filename != '':
            try:
                path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                # set the file path
                file.save(path)
                # Open the CSV file in read mode
                with open(path, 'r') as file:
                    csv_reader = csv.reader(file)
                    # Skip the header row (if present)
                    next(csv_reader)
                    # Iterate through each row in the CSV file
                    for row in csv_reader:
                        # Execute the query using executemany for efficiency
                        data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20]]
                        connection.populate("INSERT INTO properties(email, price, suburb, property, rooms, bedroom, toilets, ensuite, condi, carport, pool, furnished, cottage, power, pbackup, water, wbackup, gated, garden, address, description) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}')".format(data[0], data[1] ,data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13] ,data[14], data[15], data[16], data[17] ,data[18], data[19], data[20]))
                        return redirect("/")   
            except Exception as e:
                     flash("An error occurred:", e)
                     return render_template('rental/properties.html')    
        return render_template('rental/properties.html')    
    else:
        return render_template('rental/properties.html')
    
@app.route('/suburbs', methods=['GET', 'POST'])
def suburbs():
    if (request.method == "POST"):
        file = request.files['suburbs']
        if file.filename != '':
            try:
                path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                # set the file path
                file.save(path)
                # Open the CSV file in read mode
                with open(path, 'r') as file:
                    csv_reader = csv.reader(file)
                    # Skip the header row (if present)
                    next(csv_reader)
                    # Iterate through each row in the CSV file
                    for row in csv_reader:
                        # Execute the query using executemany for efficiency
                        data = [row[0], row[1], row[2], row[3]]
                        connection.populate("INSERT INTO suburbs(constituency, council, suburb, density) VALUES ('{}', '{}', '{}', '{}')".format(data[3], data[2], data[0], data[1]))
                        flash("The file was successfully uploaded")
                        return render_template('rental/suburbs.html')    
            except Exception as e:
                flash("An error occurred:", e)
                return render_template('rental/suburbs.html')
        flash("They is nothing to upload")
        return render_template('rental/suburbs.html')    
    else:
        return render_template('rental/suburbs.html')

@app.route("/nsuburb")
def nsuburb():
    return send_file(
        "./static/downloads/suburbs-upload-template.zip",
        mimetype="application/zip",
        download_name="suburbs-upload-template.zip",
        as_attachment=True,)

@app.route('/harare')
def harare():
   return render_template('rental/harare.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if (request.method == "POST"):
        # Create variables for easy access
        email = request.form.get('email')
        password = request.form.get('password')
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()

        # Fetch one record and return the result
        user = connection.post("SELECT * FROM users WHERE email = '{}' AND password = '{}'".format(email, password))
        print(user)
        if user:   
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user[0]
            session['email'] = user[2]
            properties =  connection.posts("SELECT * FROM properties WHERE email = '{}'".format(email))
            # Redirect to home page
            return render_template('rental/edit.html', properties = properties)
        else:
            flash('wrong credentials!', 'error')  # Flash a success message
            return render_template('auth/signin.html')
    else:
        return render_template('auth/signin.html')
    
@app.route('/signout')
def signout():
    # Remove session data, this will log the user out
    session.pop('signout', None)
    session.pop('id', None)
    session.pop('email', None)
    properties =  connection.posts("SELECT * FROM properties")
    return render_template('index.html', properties = properties) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == "POST"):
        # Output message if something goes wrong...
        msg = ''
        # Check if "email", "password" and "email" POST requests exist (user submitted form)
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')

        # Check if user exists using MySQL
        user =  connection.posts("SELECT * FROM users WHERE email = '{}'".format(email))
        
        # If user exists show error and validation checks
        if user:
            msg = 'user already exists!'
            flash(msg, 'error')
            return render_template('auth/register.html')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            flash(msg, 'error')
            return render_template('auth/register.html')
        elif not re.match(r'[A-Za-z0-9]+', email):
            msg = 'email must contain only characters and numbers!'
            flash(msg, 'error')
            return render_template('auth/register.html')
        elif not email or not password:
            msg = 'Please fill out the form!'
            flash(msg, 'error')
            return render_template('auth/register.html')
        else:
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # user doesn't exist, and the form data is valid, so insert the new user into the users table
            connection.populate("INSERT INTO users(name, email, password) VALUES ('{}','{}','{}')".format(name, email, password))
            msg = 'You have successfully registered!'
            flash(msg, 'success')
            return render_template('auth/signin.html')
    else:
        return render_template('auth/register.html')
    
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    email = session["email"]
    properties =  connection.posts("SELECT * FROM properties WHERE email = '{}'".format(email))
    if (request.method == "POST"):
        return render_template('rental/edit.html', properties = properties)
    return render_template('rental/edit.html', properties = properties)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    email = session["email"]
    connection.posts("DELETE FROM properties WHERE email = '{}'".format(email))
    if (request.method == "POST"):
        return redirect("/edit")
    
@app.route('/search')
def search(): 
    properties =  connection.posts("SELECT * FROM properties WHERE email")
    return render_template('rental/edit.html', properties = properties)
                
if __name__ == '__main__':
    app.run(debug=True)
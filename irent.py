from flask import Flask, render_template, redirect, url_for, request, session, send_file
import re, hashlib
from source.databaseConnection import Database
import os
import csv
from machine.harare.HarareRentPredictionModel import rentalPrediction
from machine.harare.PropertyPredictionModel import propertyPrediction

app = Flask(__name__, template_folder='./public')
# enable debugging mode
app.config["DEBUG"] = True
# Upload folder
app.config['UPLOAD_FOLDER'] =  'static/uploads'

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Database Connection
connection = Database(host="localhost", user="root", password="edmore1", database="irental")
connection.connect()

@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == "POST"):
        try:
            suburb = request.form.get('suburb')
            density =  "Low"
            toilet_type = request.form.get('toilet_type')
            rooms = request.form.get('rooms')
            bedrooms = request.form.get('bedrooms')
            toilets = request.form.get('toilets')
            property_type = request.form.get('properties')
            ensuites = request.form.get('ensuites')
            local_authority = "Harare Municipality" 
            ward = 17
            garage = request.form.get('garage')
            pool = request.form.get('pool')
            fixtures = request.form.get('fixtures')
            cottage = request.form.get('cottage')
            power = request.form.get('power')
            power_backup = request.form.get('power_backup')
            water = request.form.get('water')
            water_backup = request.form.get('water_backup')
            gated = request.form.get('gated')
            garden = request.form.get('garden')
        
            features = [property_type, suburb, density, toilet_type, rooms, bedrooms, toilets, ensuites, local_authority, ward, garage, pool, 
                    fixtures, cottage, power, power_backup, water, water_backup, gated, garden]
            
            print(features)
            output = rentalPrediction.userInput(features)
            #Loading model to compare the results
            #pickle.load(open('HarareRentPredictionModel.pkl','rb'
        except Exception as e:
            print("An error occurred:", e)

        return render_template('rental/output.html', price = output)
    else:
        return render_template('index.html')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
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
                        data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21]]
                        connection.populate("INSERT INTO properties(email, price, suburb, density, type_of_property, rooms, bedroom, toilets, ensuite, toilets_type, garage, swimming_pool, fixtures_fittings, cottage, power, power_backup, water, water_backup, gated_community, garden_area, address, description) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}')".format(data[0], data[1] ,data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13] ,data[14], data[15], data[16], data[17] ,data[18], data[19], data[20], data[21]))
            except Exception as e:
                     print("An error occurred:", e)
                        
        return render_template('rental/upload.html')    
    else:
        return render_template('rental/upload.html')

@app.route("/download")
def download():
    return send_file(
        "./static/downloads/properties-upload-template.zip",
        mimetype="application/zip",
        download_name="properties-upload-template.zip",
        as_attachment=True,) 

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if (request.method == "POST"):
        try:
            suburb = request.form.get('suburb')
            price = request.form.get('price')

            features = [suburb, price]

            print(features)
            output = propertyPrediction.userInput(features)
            #Loading model to compare the results
            #pickle.load(open('HarareRentPredictionModel.pkl','rb'
        except Exception as e:
            print("An error occurred:", e)

        return render_template('rental/predict.html')
    else:
        return render_template('rental/predict.html')


@app.route('/show')
def show():
    properties =  connection.posted("SELECT * FROM properties")
    return render_template('rental/show.html', properties = properties)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if (request.method == "POST"):
        # Create variables for easy access
        email = request.form.get['email']
        password = request.form.get['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()

        users =  connection.posted('SELECT * FROM users WHERE email = %s AND password = %s', [email, password])
        # Fetch one record and return the result
      
        if users:   
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = users['id']
            session['email'] = users['email']
            # Redirect to home page
        return render_template('rental/edit.html')
    else:
        return render_template('auth/signin.html')
    
@app.route('/signout')
def signout():
    # Remove session data, this will log the user out
    session.pop('signout', None)
    session.pop('id', None)
    session.pop('email', None)
    # Redirect to login page
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == "POST"):
        # Output message if something goes wrong...
        msg = ''
        # Check if "email", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'email' in request.form.get and 'password' in request.form.get and 'email' in request.form.get:
            # Create variables for easy access
            name = request.form.get['name']
            password = request.form.get['password']
            email = request.form.get['email']

            # Check if user exists using MySQL
            user =  connection.posted('SELECT * FROM users WHERE email = %s', [email] )
         
            # If user exists show error and validation checks
            if user:
                msg = 'user already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', email):
                msg = 'email must contain only characters and numbers!'
            elif not email or not password or not email:
                msg = 'Please fill out the form!'
            else:
                # Hash the password
                hash = password + app.secret_key
                hash = hashlib.sha1(hash.encode())
                password = hash.hexdigest()
                # user doesn't exist, and the form data is valid, so insert the new user into the users table
                connection.posted('INSERT INTO users(name, email, password) VALUES (%s, %s, %s)', [name, email, password])
                msg = 'You have successfully registered!'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        # Show registration form with message (if any)
        return render_template('auth/register.html')
    else:
        return render_template('auth/register.html')

if __name__ == '__main__':
    app.run(debug=True ,use_reloader=True)
    
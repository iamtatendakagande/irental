from flask import Flask, render_template, redirect, url_for, request, session, send_file, flash
import re, hashlib
from source.databaseConnection import database
import os
import pandas as pd 
import csv
from source.userInputRent import predict
from source.userInputProperty import predicted
from source.mapCreation import createHarareMap

app = Flask(__name__, template_folder='./public')
# enable debugging mode
#app.config["DEBUG"] = True
app.config['TESTING'] = True
# Upload folder
app.config['UPLOAD_FOLDER'] =  'static/uploads'

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Database Connection
connection = database(host="localhost", user="root", password="edmore1", database="irental")
connection.connect()

@app.route('/', methods=['GET'])
def index():
    properties =  connection.posts("SELECT * FROM properties")
    return render_template('/index.html', properties = properties)

@app.route('/pricepredication', methods=['GET', 'POST'])
def pricepredication():
    if (request.method == "POST"):
        file = request.files['file']
        try:
            input = pd.read_csv(file)
            print(input.iloc[0, 0])
            suburb = input.iloc[0, 0]
            record = connection.post("SELECT * FROM suburbs WHERE suburb = '{}'".format(suburb))
            if record != None:
                input.insert(10, 'council', record[1], True)
                input.insert(9, 'constituency', record[2], True)
                input.insert(1, 'density', record[4], True)     
                print(record)   
                print(input.tail())
                output = predict.userInput(input)
                # Process form data
                #flash('Your form has been submitted!', 'success')  # Flash a success message
                return render_template('rental/output.html', price = output)
            else:
                return render_template('rental/price.html') 
        except Exception as e:
            print("An error occurred:", e)
            flash("An error occurred:", 'error')
            return render_template('rental/price.html')
    else:
        return render_template('rental/price.html')
    

@app.route("/predication")
def predication():
    return send_file(
        "./static/downloads/predication-price-template.zip",
        mimetype="application/zip",
        download_name="predication-price-template.zip",
        as_attachment=True,) 
       
@app.route('/propprediction', methods=['GET', 'POST'])
def propprediction():
    if (request.method == "POST"): 
        try:
            suburb = request.form.get('suburb')
            price = request.form.get('price')

            record = connection.post("SELECT * FROM suburbs WHERE suburb = '{}'".format(suburb))
            print(record)
            if record != None:
                council = record[2]
                constituency = record[1]
                density = record[4]
                features = [suburb, density, price, constituency, council]
                print(features)
                output = predicted.userInputed(features)
                return render_template('rental/output.html', price = output)
            else:
               flash("suburb not found please download the suburbs file check spelling or upload file using the attached templated", 'error')
               return render_template('rental/property.html') 
        except Exception as e:
            print("An error occurred:", e)
            flash("An error occurred:", 'error')
            return render_template('rental/property.html')
    else:
        return render_template('rental/property.html')

    
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
                        data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21]]
                        connection.populate("INSERT INTO properties(email, price, suburb, density, property, rooms, bedroom, toilets, ensuite, type, carport, pool, furnished, cottage, power, pbackup, water, wbackup, gated, garden, address, description) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}')".format(data[0], data[1] ,data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13] ,data[14], data[15], data[16], data[17] ,data[18], data[19], data[20], data[21]))
                
                append = './machine/harare/updated.csv'
                with open(append, 'a', newline='') as appended:
                    csv_writer = csv.writer(appended)
                    line = [row[2], row[3], row[4], row[7], row[1], row[5], row[6], 'NULL', row[8], 'NULL', row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20]]
                    csv_writer.writerow(line)
            except Exception as e:
                     print("An error occurred:", e)
                     flash("An error occurred:", 'error')
        return render_template('rental/properties.html')    
    else:
        return render_template('rental/properties.html')

@app.route("/coordinate")
def coordinate():
    return send_file(
        "./static/downloads/coordinates-upload-template.zip",
        mimetype="application/zip",
        download_name="coordinates-upload-template.zip",
        as_attachment=True,) 

@app.route('/coordinates', methods=['GET', 'POST'])
def coordinates():
    if (request.method == "POST"):
        file = request.files['coordinates']
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
                        # Create the POINT object using MySQL's ST_PointFromText function
                        point = f"POINT({data[3]},{data[2]})"
                        print(point)
                        connection.populate("DELETE FROM coordinates")
                        connection.populate("INSERT INTO coordinates(address, council, coordinates) VALUES ('{}', '{}', {})".format(data[0], data[1], point))
            except Exception as e:
                     print("An error occurred:", e)
                     flash('Your form has been submitted!', 'error')
        createHarareMap.map()
        return render_template('rental/map.html')    
    else:
        return render_template('rental/coordinates.html')
    
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
                        connection.populate("INSERT INTO suburbs(constituency, council, suburb, density) VALUES ('{}', '{}', '{}', '{}')".format(data[0], data[1], data[2], data[3]))
            except Exception as e:
                     print("An error occurred:", e)
        flash('Your form has been submitted!', 'success')
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

@app.route('/map')
def map():
   return render_template('rental/map.html')

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
            connection.populate("INSERT INTO users(name, email, password) VALUES ('{}','{}','{}')".format(name, email, password))
            msg = 'You have successfully registered!'
        flash(msg, 'error')  # Flash a success message
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
    properties =  connection.posts("DELETE FROM properties WHERE email = '{}'".format(email))
    if (request.method == "POST"):
        return render_template('rental/edit.html', properties = properties)
    return render_template('rental/edit.html', properties = properties)
    
@app.route('/search')
def search(): 
    properties =  connection.posts("SELECT * FROM properties WHERE email")
    return render_template('rental/edit.html', properties = properties)
                
if __name__ == '__main__':
    app.run(debug=True)
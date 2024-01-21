from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
import pickle

#from machine.HarareRentPredictionModel import userInput


app = Flask(__name__, template_folder='./public')

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'edmore1'
app.config['MYSQL_DB'] = 'irental'
 
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == "POST"):
        return render_template('index.html')
    else:
        return render_template('index.html')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if (request.method == "POST"):


        
        return render_template('rental/upload.html')
    else:
        return render_template('rental/upload.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if (request.method == "POST"):
        # Loading model to compare the results
        #pickle.load(open('HarareRentPredictionModel.pkl','rb'))
        
        suburb = request.form['suburb']
        density =  "Low"
        toilets_type = "Self"
        rooms = request.form['rooms']
        bedroom = request.form['bedroom']
        toilets = request.form['toilets']
        ensuite = 0
        local_authority = "Harare Municipality"
        ward = 17
        garage = 1
        swimming_pool = 0
        fixtures_fittings = 1
        cottage = 1
        power = 1
        power_backup = 1
        water = 1
        water_backup = 1
        gated_community = 0
        garden_area = 1
        
        features =  [ suburb, density, toilets_type, rooms, bedroom, toilets, ensuite, local_authority, ward, garage, swimming_pool, 
                     fixtures_fittings, cottage, power, power_backup, water, water_backup, gated_community, garden_area]

        #features = userInput(features)

        return render_template('rental/predict.html')
    else:
        return render_template('rental/predict.html')

@app.route('/map')
def map():
    import folium

    # Center coordinates of Harare Metropolitan Province (replace with exact coordinates if needed)
    latitude = -17.825166
    longitude = 31.053056

    # Create a base map
    map = folium.Map(location=[latitude, longitude], zoom_start=11)

    # Coordinate points (replace with your actual list of points)
    points = [
        [-17.8154, 31.0456],  # Example point 1
        [-17.8352, 31.0625],  # Example point 2
        # ... Add more points as needed
    ]

    # Add markers for each point
    for point in points:
        folium.Marker(location=point).add_to(map)


    # Display the map
    file_name = 'public/rental/'
    map.save(file_name+"harare.html")  # Save the map as an HTML file
    return render_template('rental/map.html')

@app.route('/harare')
def showMap():
    return render_template('rental/harare.html')

@app.route('/show')
def show():
    return render_template('rental/show.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if (request.method == "POST"):
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()

        # Check if users exists using MySQLusers
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', [email, password])
        # Fetch one record and return the result
        users = cursor.fetchone()

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
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']

            # Check if user exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s', [email] )
            user = cursor.fetchone()
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
                cursor.execute('INSERT INTO users(name, email, password) VALUES (%s, %s, %s)', [name, email, password])
                mysql.connection.commit()
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
    
requirements
$ postgreSQL
$ python

important but not requirements
$ vscode with jupyter notebook

(On Mac/Linux)
$ mkdir myproject
$ cd myproject
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install Flask

(On Windows CMD)
> mkdir myproject
> cd myproject
> py -3 -m venv .venv
> .venv\Scripts\activate
$ pip install Flask

$ pip install --missing libraries check in errors--

dropdb irental
createdb irental

# This PostgreSQL command creates the empty database
# (On Mac/Linux)
export FLASK_APP=app.py
#eg. export FLASK_APP=irent.py
export DATABASE_URL='postgresql://postgres:password@localhost:5432/your_db_name'
#eg.export DATABASE_URL='postgresql://tkagande:@127.0.0.1/irental'

# (On Windows CMD)
set FLASK_APP=app.py
#eg. set FLASK_APP=irent.py
set DATABASE_URL="postgresql://postgres:password@localhost:5432/your_db_name"
#eg.DATABASE_URL='postgresql://tkagande:@127.0.0.1/irental'

flask db init
flask db migrate -m "first database creation"
flask db upgrade

#run the application
flask --app irent run  

# my_app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 1. Create the extension instances WITHOUT an app
#    These objects will be "bound" to our app later in the factory.
db = SQLAlchemy()
migrate = Migrate()


# 2. Define all your models
#    This code is pasted directly from your original file.

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
    suburb = db.Column(db.String(45), nullable=False)
    density = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self):
        return f'<Suburb {self.suburb}>'

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(35), nullable=False)
    price = db.Column(db.Numeric(16, 2), nullable=False)
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

    def __repr__(self):
        return f'<Property {self.address}>'
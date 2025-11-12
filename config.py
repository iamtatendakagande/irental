import os
from dotenv import load_dotenv

load_dotenv() 
FLASK_APP = os.environ.get('FLASK_APP')

# --- Database ---
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check your .env file.")

SQLALCHEMY_DATABASE_URI = DATABASE_URL

SQLALCHEMY_TRACK_MODIFICATIONS = False
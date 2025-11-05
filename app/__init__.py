# my_app/__init__.py

from flask import Flask
from .models import db, migrate  # Import from your models.py
import config

def create_app():
    """Create and configure the Flask application."""
    
    app = Flask(__name__)
    
    # 1. Load configuration from config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 2. Initialize the extensions WITH the app
    #    This "binds" the db and migrate objects to your app.
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 3. Register your custom CLI command
    register_cli_commands(app)

    # 4. Import your models
    #    This is crucial so that SQLAlchemy and Flask-Migrate 
    #    know about your models.
    with app.app_context():
        from . import models

    # 5. Register your blueprints (routes) here (when you have them)
    # from . import routes
    # app.register_blueprint(routes.my_blueprint)

    return app


def register_cli_commands(app):
    """Registers the 'flask checkdb' command."""
    
    @app.cli.command("checkdb")
    def check_db_connection():
        """Checks if the database connection is valid."""
        try:
            # db.engine is available because we initialized db with the app
            with db.engine.connect() as connection:
                connection.execute(db.text("SELECT 1"))
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed:")
            print(f"\n{e}")
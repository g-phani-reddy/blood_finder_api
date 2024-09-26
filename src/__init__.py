from flask import Flask
from src.extensions import db 
import os

from src.controllers.user import user_bp

def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['DEBUG'] = os.getenv('DEBUG', 'True') == 'True'

    # Initialize the database with the app
    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix="/user")

    return app

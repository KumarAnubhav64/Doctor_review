from flask import Flask
from app.routes import review_blueprint
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)

    # Register the review blueprint
    app.register_blueprint(review_blueprint)

    # Initialize MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    app.db = client['hospitalDb']  # MongoDB database

    return app

import os
from typing import Any

from flask import Flask
from routes import pages
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app() -> Any:
    app: Flask = Flask(__name__)
    client: MongoClient = MongoClient(os.environ.get("MONGODB_URI"))
    app.db: Any = client.get_default_database()
    
    app.register_blueprint(pages)
    return app
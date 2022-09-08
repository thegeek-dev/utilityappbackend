from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
import os
import dotenv
from mailjet_rest import Client

PORT = os.environ.get('PORT') or dotenv.get_key(
    key_to_get="PORT", dotenv_path=".env")

MONGO_URI = os.environ.get('MONGO_URI') or dotenv.get_key(
    dotenv_path="./.env", key_to_get="MONGO_URI")

mailjet_api_key = os.environ.get('MAILJET_API_KEY') or dotenv.get_key(
    dotenv_path="./.env", key_to_get="MAILJET_API_KEY")

mailjet_api_secret = os.environ.get('MAILJET_API_SECRET') or dotenv.get_key(
    dotenv_path="./.env", key_to_get="MAILJET_API_SECRET")

app = Flask(__name__)
api = Api(app)
mongodb_client = PyMongo(app, MONGO_URI)
db = mongodb_client.db
mailjet = Client(auth=(mailjet_api_key, mailjet_api_secret), version='v3.1')

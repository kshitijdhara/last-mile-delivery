from flask import Flask
import pyrebase
from firebase_admin import firestore, credentials, initialize_app

from app import config


application = Flask(__name__)


# set up firebase configs for firebase authentication
firebase_config = config.firebaseConfig
pb = pyrebase.initialize_app(firebase_config)
auth = pb.auth()

# set up firestore credentials and database
cred = credentials.Certificate("app/firestore_config.json")
default_app = initialize_app(cred)
db = firestore.client()
vehicle_collection = db.collection("vehicle") # firestore vehicle collection

from app import (
    server,
    config,
    auth,
    profile
    )
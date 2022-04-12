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

order_collection = db.collection("orders") # order database

depot= "PICT Pune"

from app import (
    server,
    config,
    authentication,
    profile,
    database,
    distance_matrix,
    vrp,
    maps
    )

# from flask_mail import Mail, Message

# # mail = Mail(application) # instantiate the mail class

# # configuration of mail
# application.config['MAIL_SERVER']='smtp.gmail.com'
# application.config['MAIL_PORT'] = 465
# application.config['MAIL_USERNAME'] = 'dharakshitij@gmail.com'
# application.config['MAIL_PASSWORD'] = 'qayiguqhodoxumcf'
# application.config['MAIL_USE_TLS'] = False
# application.config['MAIL_USE_SSL'] = True
# mail = Mail(application)


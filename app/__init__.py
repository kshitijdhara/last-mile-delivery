from flask import Flask
import pyrebase

from app import config


application = Flask(__name__)


# set up firebase configs for firebase authentication
firebase_config = config.firebaseConfig
pb = pyrebase.initialize_app(firebase_config)
auth = pb.auth()


from app import (
    server,
    config
    )
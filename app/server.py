from app import application
from flask import Flask

# api for base route 
@application.route('/', methods=['GET'])
def hello():
    return "Last Mile Delivery server running on localhost:8080"

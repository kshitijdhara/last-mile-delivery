from app import application
from flask import Flask

@application.route('/', methods=['GET'])
def hello():
    return "Last Mile Delivery server running on localhost:8080"

from app import application
from flask import Flask

@application.route('/', methods=['GET'])
def hello():
    return "Hello World"

from werkzeug.wrappers import response
from app import application, auth


from flask import Flask, request



@application.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        try: 
            data = request.form
            email = data.get('email')
            password = data.get('password')

            user = auth.sign_in_with_email_and_password(email, password)

            uid = user['localId']

            return uid
        except Exception as e:
            response = {"type": "Login Failed","msg": e}
            return response


@application.route("/changepwd", methods=['POST'])
def change_password():
    if request.method == 'POST':
        try: 
            data = request.form
            email = data.get('email')
            auth.send_password_reset_email(email)
            response = {"type": "Success","msg": "password reset emai sent"}
            return response
        except Exception as e:
            response = {"type": "Password Reset Failed","msg": e}
            return response
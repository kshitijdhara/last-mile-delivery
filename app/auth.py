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
            response = {
                "status": "Success",
                "type": "Login Success",
                "msg": uid
                }
            return response
        except Exception as e:
            response = {
                "status": "Failed",
                "type": "Login Failed",
                "msg": e
                }
            return response


@application.route("/changepwd", methods=['POST'])
def change_password():
    if request.method == 'POST':
        try: 
            data = request.form
            email = data.get('email')
            auth.send_password_reset_email(email)
            response = {
                "status": "Success",
                "type": "Password Change Success",
                "msg": "password reset email sent"
                }
            return response
        except Exception as e:
            response = {
                "status": "Failed",
                "type": "Password Reset Failed",
                "msg": e
                }
            return response
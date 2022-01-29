from pkg_resources import register_namespace_handler
from app import application, vehicle_collection

from flask import Flask, request,jsonify



# api to update profile using UID as document id
@application.route('/updateprofile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        try:
            result = request.form
            data = {
                "uid": result.get ('uid'),
                "email": result.get('email'),
                "name": result.get('name'),
                "contact": result.get('contact'),
                "address": result.get('address'),
                "driver_license": result.get('dl'),
                "vehicle_number": result.get('vno'),
                "vehicle_rc": result.get('vrc'),
                "status": "away"
            }
            print("Data => ")
            print(data)
            uid = result.get("uid")
            print("UID =>  " + uid)
            vehicle_collection.document(uid).set(data)
            response = {
                "status": "Success",
                "type": "Update Profile Success",
                "msg": data
                }
            return response

        except Exception as e:
            response = {
                "status": "Failed",
                "type": "Update Profile Failed",
                "msg": e
                }
            return response


# api to get the vehicle profile using UID as input 
@application.route('/profile/<uid>', methods=['GET'])
def get_profile(uid):
    if request.method == 'GET':
        try:
            profile = vehicle_collection.document(uid).get().to_dict()
            print(profile)
            response = {
              "status": "Success",
              "type": "Get Profile Success",
              "msg": profile  
            }
            return response
        except Exception as e:
            response = {
                "status": "Failed",
                "type": "Get Profile Failed",
                "msg": e
                }
            return response

@application.route('/updatestatus', methods=['POST'])
def update_status():
    if request.method == 'POST':
        try:
            result = request.form
            data = {
                "status": result.get("status")
            }
            print("Data => ")
            print(data)
            uid = result.get("uid")
            print("UID =>  " + uid)
            vehicle_collection.document(uid).update(data)
            response = {
                "status": "Success",
                "type": "Update Profile Status Success",
                "msg": data
                }
            return response

        except Exception as e:
            response = {
                "status": "Failed",
                "type": "Update Profile Status Failed",
                "msg": e
                }
            return response
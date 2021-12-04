from app import application, vehicle_collection

from flask import Flask, request



# api to update profile using UID as document id
@application.route('/updateprofile',methods=['POST'])
def update_profile():
    if request.method == 'POST':
        try:
            result = request.form()
            data = {
                "uid" : result.get ("uid"),
                "email" : result.get("email"),
                "name" : result.get("name"),
                "contact": result.get("contact"),
                "address": result.get("address"),
                "driver_license": result.get("dl"),
                "vehicle_number" : result.get("vno"),
                "vehicle_rc": result.get("vrc"),
                "status": "away", # away or active


            }
            uid = result.get("uid")
            vehicle_collection.document(uid).update(data)

        except Exception as e:
            response = {
                "status": "Failed",
                "type": "Update Profile Failed",
                "msg": e
                }
            return response


# api to get the vehicle profile using UID as input 
@application.route('/profile/<uid>',methods=['GET'])
def get_profile(uid):
    if request.method == 'GET':
        try:
            profile = vehicle_collection.document(id).get().to_dict()
            response = {
              "status": "Success",
              "type": "Get Profile Success",
              "msg": profile  
            }
        except Exception as e:
            response = {
                "status": "Failed",
                "type": "Get Profile Failed",
                "msg": e
                }
            return response
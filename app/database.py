from flask.json import jsonify
from app import application, order_collection
import requests
from flask import request

import re



@application.route('/getorders', methods=['GET'])
def get_orders():
    if request.method == 'GET':
        try:
            data = order_collection.order_by(u'order_date').stream()
            active_orders = dict()
            for doc in data:
                # print(doc.to_dict())
                active_orders[doc.id] = doc.to_dict() 


            response = {
                "status": "Success",
                "type": "Get orders Success",
                "msg": active_orders
            }
            return response


        except Exception as e:
            response = {
                "status": "Failed",
                "type": "Get orders Failed",
                "msg": e
            }
            return response

@application.route("/lol")
def get_address():
    delivery_locations = list()
    delivery_locations.append("MG+Road+Camp+Pune")
    orders = get_orders()['msg']
    print(orders)
    for key,value in orders.items():
        print(key)
        print(value)
        value['shop_address'] = re.sub(r"\W+","+",value['shop_address'])
        value['customer_address'] = re.sub(r"\W+","+",value['customer_address'])
        delivery_locations.append(value['shop_address'])
        delivery_locations.append(value['customer_address'])

    print(delivery_locations)
    print(len(delivery_locations))
    return delivery_locations
    # return orders
    # return jsonify(delivery_locations)
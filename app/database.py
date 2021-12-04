from app import application, order_collection
import requests
from flask import request
@application.route('/getorders', methods=['GET'])
def get_orders():
    if request.method == 'GET':
        try:
            data = order_collection.order_by(u'order_date').get()
            active_orders = dict()
            for doc in data:
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


def get_address(orders):
    delivery_locations = list()
    for i in orders:
        delivery_locations.append(i['customer_address'])

    print(delivery_locations)

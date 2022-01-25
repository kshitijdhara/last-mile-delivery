from __future__ import division
from __future__ import print_function
from crypt import methods
import requests
import json
import urllib
from app import config, database, depot, application


def create_data():
  """Creates the data."""
  data = dict()
  data['API_key'] = config.G_API_KEY
  # data['addresses'] = [ # depot
  #                      '1921+Elvis+Presley+Blvd+Memphis+TN',
  #                      '149+Union+Avenue+Memphis+TN',
  #                      '1034+Audubon+Drive+Memphis+TN',
  #                      '1532+Madison+Ave+Memphis+TN',
  #                      '706+Union+Ave+Memphis+TN',
  #                      '3641+Central+Ave+Memphis+TN',
  #                      '926+E+McLemore+Ave+Memphis+TN',
  #                      '4339+Park+Ave+Memphis+TN',
  #                      '600+Goodwyn+St+Memphis+TN',
  #                      '2000+North+Pkwy+Memphis+TN',
  #                      '262+Danny+Thomas+Pl+Memphis+TN',
  #                      '125+N+Front+St+Memphis+TN',
  #                      '5959+Park+Ave+Memphis+TN',
  #                      '814+Scott+St+Memphis+TN',
  #                      '1005+Tillman+St+Memphis+TN'
  #                     ]
  data['addresses'] = database.get_address()
  print(f'data = {data}')
  return data

def create_distance_matrix(data):
  addresses = data["addresses"]
  API_key = data["API_key"]
  # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
  max_elements = 100
  num_addresses = len(addresses) # 16 in this example.
  # Maximum number of rows that can be computed per request (6 in this example).
  max_rows = max_elements // num_addresses
  # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
  q, r = divmod(num_addresses, max_rows)
  dest_addresses = addresses
  distance_matrix = []
  # Send q requests, returning max_rows rows per request.
  for i in range(q):
    origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)

  # Get the remaining remaining r rows, if necessary.
  if r > 0:
    origin_addresses = addresses[q * max_rows: q * max_rows + r]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)
    print(f'distance matrix = {distance_matrix}')
  return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
  """ Build and send request for the given origin and destination addresses."""
  def build_address_str(addresses):
    # Build a pipe-separated string of addresses
    address_str = ''
    for i in range(len(addresses) - 1):
      address_str += addresses[i] + '|'
    address_str += addresses[-1]
    return address_str

  request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_address_str(origin_addresses)
  dest_address_str = build_address_str(dest_addresses)
  request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
  jsonResult = urllib.request.urlopen(request).read()
  response = json.loads(jsonResult)
  return response

def build_distance_matrix(response):
  distance_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
  return distance_matrix

@application.route('/distance', methods=['GET'])
def dd():
    # """Entry point of the program"""
    # Create the data.
    data = create_data()
    addresses = data['addresses']
    API_key = data['API_key']
    distance_matrix = create_distance_matrix(data)
    print(distance_matrix)    
    addresses = data['addresses']   
    pickup_deliveries = list()
    addresses.remove("depot")
    print(addresses)
    pickup_deliveries = list()
    i = 1
    while len(addresses):
        temp_list = list()
        for val in addresses:
            temp_list.append(i)
            i = i + 1
            if len(temp_list) == 2:
                break
        pickup_deliveries.append(temp_list)
        addresses.pop(0)
        addresses.pop(0)    
    print(pickup_deliveries)
    return distance_matrix

# # dummy output for distance matrix 
# distance_matrix = [
#         [
#             0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
#             468, 776, 662
#         ],
#         [
#             548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
#             1016, 868, 1210
#         ],
#         [
#             776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
#             1130, 788, 1552, 754
#         ],
#         [
#             696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
#             1164, 560, 1358
#         ],
#         [
#             582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
#             1050, 674, 1244
#         ],
#         [
#             274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
#             514, 1050, 708
#         ],
#         [
#             502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
#             514, 1278, 480
#         ],
#         [
#             194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
#             662, 742, 856
#         ],
#         [
#             308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
#             320, 1084, 514
#         ],
#         [
#             194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
#             274, 810, 468
#         ],
#         [
#             536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
#             730, 388, 1152, 354
#         ],
#         [
#             502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
#             308, 650, 274, 844
#         ],
#         [
#             388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
#             536, 388, 730
#         ],
#         [
#             354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
#             342, 422, 536
#         ],
#         [
#             468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
#             342, 0, 764, 194
#         ],
#         [
#             776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
#             388, 422, 764, 0, 798
#         ],
#         [
#             662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
#             536, 194, 798, 0
#         ],
#     ]

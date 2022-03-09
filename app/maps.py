from app import application, vrp, database

from flask import request


@application.route('/map', methods=['GET'])
def map():
    if request.method == 'GET':
        
        # routes for dev
        temp_dict = {
            0:  [0,1,3,2,4,0],
            1:  [0,5,8,7,6,0],
            2:  [0,5,8,7,6,0],
            3:  [0,5,8,7,6,0],
        }

        # get the route of each vehicle from the VRP function

        temp_data = vrp.vrp_main()
        
        # temp_data = temp_dict # for dev
        
        plan_dict = temp_data ['msg']

        # plan_dict = temp_data # for dev
        print("-------------------- MAPS -------------------")
        print(plan_dict)
        print(type(plan_dict))


        # get the addresses list from the get_address() function

         # addresses for dev 

        # addresses = [          '1005+Tillman+St+Memphis+TN', # depot
        #                        '1921+Elvis+Presley+Blvd+Memphis+TN',
        #                        '149+Union+Avenue+Memphis+TN',
        #                        '1034+Audubon+Drive+Memphis+TN',
        #                        '1532+Madison+Ave+Memphis+TN',
        #                        '706+Union+Ave+Memphis+TN',
        #                        '3641+Central+Ave+Memphis+TN',
        #                        '926+E+McLemore+Ave+Memphis+TN',
        #                        '4339+Park+Ave+Memphis+TN',
        #                        '600+Goodwyn+St+Memphis+TN',
        #                        '2000+North+Pkwy+Memphis+TN',
        #                        '262+Danny+Thomas+Pl+Memphis+TN',
        #                        '125+N+Front+St+Memphis+TN',
        #                        '5959+Park+Ave+Memphis+TN',
        #                        '814+Scott+St+Memphis+TN',
        #                        '1005+Tillman+St+Memphis+TN'
        #                       ]
        
        
        addresses = database.get_address()
        print(addresses)

        # below is the code to subsitute the indexes of the route each vehicle is supposed to take by their respective addresses
        route_address_dict = dict()

        for key,value in plan_dict.items():
            temp_list = list()
            for i in value:
                temp_list.append(addresses[i])
            print(temp_list)
            route_address_dict[key] = temp_list
        
        print("-----------------------------------------------")
        print(route_address_dict)
        print("-----------------------------------------------")
        

        # below is the code to convert the route of each vehicle to a navigable url
        url_dict = dict()
        for key, value in route_address_dict.items():
            depot = addresses[0]
            print(depot)
            url = f'https://www.google.com/maps/dir/?api=1&origin={depot}&destination={depot}&travelmode=driving&waypoints=via:'
            value.pop(0)
            value.pop(len(value)-1)
            print(value)
            final_url = url
            for i in value:
                print(url)
                final_url = final_url + i + "|"
                print(final_url)
            url_dict[key]= final_url
        print(url_dict)
        # return route_address_dict
        return url_dict
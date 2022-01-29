from app import application, vrp

from flask import request


@application.route('/map', methods='POST')
def map():
    if request.method == 'POST':
        temp_dict = {
            0:  [0,1,3,2,4,0],
            1:  [0,5,8,7,6,0],
            2:  [0,5,8,7,6,0],
            3:  [0,5,8,7,6,0],
        }

        temp_data = vrp.vrp_main()['msg']
        plan_dict = temp_data['solution']
        print(plan_dict)
        print(type(plan_dict))
        # addresses = ["depot", # depot
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
        addresses = temp_data['addresses']
        final_dict = dict()

        for key,value in plan_dict.items():
            temp_list = list()
            for i in value:
                temp_list.append(addresses[i])
            print(temp_list)
            final_dict[key] = temp_list

        print(final_dict)
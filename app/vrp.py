"""Simple Pickup Delivery Problem (PDP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


from app import application, distance_matrix, database


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # temp_data = {"msg":{
    #     "pickup_deliveries":[[1, 2], [3, 4]],
    #     "distance_matrix":[
    #         [0, 11192, 10420, 9585, 10420],
    #         [11974, 0, 4637, 3920, 4637],
    #         [11469, 4510, 0, 1083, 0],
    #         [10601, 3642, 745, 0, 745],
    #         [11469, 4510, 0, 1083, 0]],
    # }}

    temp_data = distance_matrix.dd()
    data['distance_matrix'] = temp_data['msg']['distance_matrix']
    data['pickups_deliveries'] = temp_data['msg']['pickup_deliveries']
    data['num_vehicles'] = database.get_vehicles()['msg']['number_of_vehicles']
    data['depot'] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    plan_dict = dict()
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        plan_list = list()
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            plan_list.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_dict[vehicle_id] = plan_list
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        total_distance += route_distance
    print('Total Distance of all routes: {}m'.format(total_distance))
    print('\n\n\n Plan dict ===> ')
    print(plan_dict)
    return plan_dict


# api to calculate the route based on the available delivery vehicles and the current active orders 
@application.route('/vrp')
def vrp_main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        30000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Define Transportation Requests.
    for request in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(
                delivery_index))
        routing.solver().Add(
            distance_dimension.CumulVar(pickup_index) <=
            distance_dimension.CumulVar(delivery_index))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        msg = print_solution(data, manager, routing, solution)
        response = {
            "msg": msg,
            "type": "VRP success",
            "status": "Success"
        }
    else:
        msg = 'No solution found'
        response = {
        "msg": msg,
        "type": "VRP failed",
        "status": "Failed"
    }
    print('----------------- VRP RESPONSE --------------------')
    print(response)
    print(data)
    return response
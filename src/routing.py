#!/usr/bin/env python
"""
PROJECT:
    Perch_VRP

CODE:
    routing.py

SUMMARY:
    Contains the functionality to send a request to google's OR Tools API

DOCS:
    None

DEPENDENCIES:
    None

LAST EDITED:
    2020-11-09  Created - Louise

CONTACT:
    Louise Kirkham <louisek@gmail.com.com>

REPO:
    https://github.com/LNKirkham/perch_vrp

"""
from __future__ import division
from __future__ import print_function
from config import API_KEY
import pandas as pd
from filepaths import FILEPATHS
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import logging
import logger_config
logger = logging.getLogger(__name__)


def create_data_model(distance_matrix, dispatch_crew_df):
    """
    Stores the data for the problem.

    """
    logger.info('Running: create_data_model()')

    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = len(dispatch_crew_df)
    data['depot'] = 0 # index of collection point location
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console.
    Also creates solution dictionary
    """

    solution_dict = {}

    max_route_distance = 0

    for vehicle_id in range(data['num_vehicles']):

        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0

        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)

        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)

        max_route_distance = max(route_distance, max_route_distance)

    print('Maximum of the route distances: {}m'.format(max_route_distance))

def get_routes(solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""

    logger.info('Running: get_routes()')


    # Get vehicle routes and store them in a two dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = []
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes

def get_route_number_of_collection_point(current_route_number, routes_without_collection_point):
    """
    For a given collection point return a tuple of (route number, order of collection point in route)
    """

    logger.info('Running: get_route_number_of_collection_point()')

    for route_num, route in enumerate(routes_without_collection_point):
        if current_route_number in route:
            return int(route_num), route.index(current_route_number)

def process_routes_from_solution(solution, routing, manager):
    """Processses routes from the solution"""

    logger.info('Running: process_routes_from_solution()')

    # Convert solution to list of routes as lists
    routes = get_routes(solution, routing, manager)

    # Remove collecton point from routes
    routes_without_collection_point = [route[1:-1] for route in routes]

    # Drop empty routes
    routes_without_collection_point = [route for route in routes_without_collection_point if route]

    return routes_without_collection_point


def add_routes_to_df(selected_locations_df, routes_without_collection_point):
    """
    Add a new columns to the original dataframe for route number and order in route for a given collection point row
    :return:
    """
    logger.info('Running: add_routes_to_df()')

    # Create column from index number (index zero is actually the collection point,
    # so delivery points have numbers matching id_num)
    selected_locations_df = selected_locations_df.reset_index().rename(columns={'index': 'route_num_order'})

    # Use index number (delivery number) to find which route it's in
    selected_locations_df['route_num_order'] = selected_locations_df['route_num_order'].apply(
        lambda x: get_route_number_of_collection_point(x, routes_without_collection_point))

    # Drop the collection point row
    selected_locations_df = selected_locations_df[~selected_locations_df['id_num'].str.contains('collect')]

    # Split out route number and order into two columns
    selected_locations_df['route_num'] = selected_locations_df['route_num_order'].apply(lambda x: x[0])
    selected_locations_df['order'] = selected_locations_df['route_num_order'].apply(lambda x: x[1])

    # Sort values by route number and order
    selected_locations_df = selected_locations_df.sort_values(by=['route_num', 'order'])


    return selected_locations_df


def run_routing(distance_matrix, dispatch_crew_df, selected_locations_df):

    logger.info('Running: run_routing()')

    # Create the data object for the model
    data = create_data_model(distance_matrix, dispatch_crew_df)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""

        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        # print_solution(data, manager, routing, solution)

        # Create array of routes from solution
        routes_without_collection_point = process_routes_from_solution(solution, routing, manager)
        print(routes_without_collection_point)

        # Add route and order of collection point to collection
        selected_locations_solution_df = add_routes_to_df(selected_locations_df, routes_without_collection_point)

        selected_locations_solution_df.to_csv(FILEPATHS['selected_locations_solution'], index=False)

    print(selected_locations_solution_df)
    return selected_locations_solution_df


if __name__ == '__main__':

    distance_matrix_df = pd.read_csv(FILEPATHS['distance_matrix'], index_col=False)
    distance_matrix = distance_matrix_df.values.tolist()
    dispatch_crew_df = pd.read_csv(FILEPATHS['dispatchers'], index_col=False)
    selected_locations_df = pd.read_csv(FILEPATHS['selected_locations'], index_col=False)

    selected_locations_solution_df = run_routing(distance_matrix, dispatch_crew_df, selected_locations_df)


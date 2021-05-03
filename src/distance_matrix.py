#!/usr/bin/env python
"""
PROJECT:
    Perch_VRP

CODE:
    distance_matrix.py

SUMMARY:
    Contains the functionality to send a request to google's distance matrix api

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
import json
import urllib.request
from config import API_KEY
import pandas as pd
from filepaths import FILEPATHS
import logging
import logger_config
logger = logging.getLogger(__name__)


def create_data(basic_locations_df):
    """
    Creates the data for the distance matrix API.
    """
    logger.info('Running: create_data()')

    data = {}
    data['addresses'] = list(basic_locations_df['api_address'])
    return data


def send_request(origin_addresses, dest_addresses, API_key):
    """
    Build and send request for the given origin and destination addresses.
    """
    logger.info('Running: send_request()')

    # dest_addresses = ['25 Coniston Walk, London, E9 6EP']
    # origin_addresses = ['33 Lancaster Avenue, LOndon SE27 9EL']

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
    """
    Creates a distance matrix from the api responses
    """
    logger.info('Running: build_distance_matrix()')

    distance_matrix = []

    for row in response['rows']:
        row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)

    return distance_matrix


def create_distance_matrix(data):
    """
    Given a list of addresses, queries the google distance matrix api to get a distance matrix - a matrix of distances
    from every address to every other address.
    :param data: data dicionary
    :return: a list per location contaiing the distance to every other location (list of lists)
    """

    logger.info('Running: create_distance_matrix()')

    addresses = data["addresses"]

    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses)  # 16 in this example.

    # Maximum number of rows that can be computed per request (6 in this example).
    max_rows = max_elements // num_addresses

    # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []

    # Send q requests, returning max_rows rows per request.
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_KEY)
        distance_matrix += build_distance_matrix(response)

    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_KEY)
        distance_matrix += build_distance_matrix(response)

        return distance_matrix

def run_distance_matrix(selected_locations_df):
    """
    Generates a new distance matrix R.
    :param selected_locations_df: dataframe of all location points to consider
    :param request_new: Boolean value of True to create new, False to read in previously created
    :return: distance matrix as list of lists
    """
    logger.info('Running: run_distance_matrix()')

    data = create_data(selected_locations_df)
    distance_matrix = create_distance_matrix(data)

    # Convert to dataframe and save as csv
    distance_matrix_df = pd.DataFrame(distance_matrix)
    distance_matrix_df.to_csv(FILEPATHS['distance_matrix'], index=False)

    return distance_matrix



if __name__ == '__main__':
    selected_locations_df = pd.read_csv(FILEPATHS['selected_locations'], index_col=False)
    run_distance_matrix(selected_locations_df)
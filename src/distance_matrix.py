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


def create_data(basic_locations_df):
    """Creates the data for the distance matrix API."""
    data = {}
    data['addresses'] = list(basic_locations_df['api_address'])
    return data


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
              dest_address_str + '&key=' + API_KEY

    jsonResult = urllib.request.urlopen(request).read()
    response = json.loads(jsonResult)

    return response


def build_distance_matrix(response):
    """Creates a distance matrix from the api responses
    """
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

if __name__ == '__main__':

    main()
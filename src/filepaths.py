#!/usr/bin/env python
"""
PROJECT:
    Perch_VRP

CODE:
    filepaths.py

SUMMARY:
    Contains the paths for all files and directories used in the codebase

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

import os


DIRECTORIES = {
    'data': '/Users/louisekirkham/Documents/personal/perch_vrp/data'
}

FILEPATHS = {
    'credentials': os.path.join(DIRECTORIES['data'], 'credentials.yml'),
    'delivery_points': os.path.join(DIRECTORIES['data'], '10_random_delivery_points.csv'),
    'dispatchers': os.path.join(DIRECTORIES['data'], 'dispatch_crew.csv'),
    'log': os.path.join(DIRECTORIES['data'], 'app.log'),
    'distance_matrix': os.path.join(DIRECTORIES['data'], 'distance_matrix.csv'),
    'selected_locations': os.path.join(DIRECTORIES['data'], 'selected_locations.csv'),
    'selected_locations_solution': os.path.join(DIRECTORIES['data'], 'selected_locations_solution.csv')

}


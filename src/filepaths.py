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

local_data_path = '/Users/louisekirkham/Documents/personal/perch_vrp/data'

local_api_key = os.path.join(local_data_path, 'credentials.yml')

DIRECTORIES = {
    'input': os.path.join(local_data_path, 'input'),
    'logs': os.path.join(local_data_path, 'logs'),
    'interim': os.path.join(local_data_path, 'interim'),
    'output': os.path.join(local_data_path, 'output'),
}

FILEPATHS = {
    'credentials': os.path.join(DIRECTORIES['input'], 'credentials.yml'),
    'delivery_points': os.path.join(DIRECTORIES['input'], '20_random_delivery_points.csv'),
    'dispatchers': os.path.join(DIRECTORIES['input'], 'dispatch_crew.csv'),
    'log': os.path.join(DIRECTORIES['logs'], 'app.log'),
    'distance_matrix': os.path.join(DIRECTORIES['interim'], 'distance_matrix.csv'),
    'selected_locations': os.path.join(DIRECTORIES['interim'], 'selected_locations.csv'),
    'selected_locations_solution': os.path.join(DIRECTORIES['output'], 'selected_locations_solution.csv'),
    'solution_plot': os.path.join(DIRECTORIES['output'], 'solution_plot.html'),
}


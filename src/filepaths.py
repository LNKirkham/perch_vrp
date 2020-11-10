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
    'data': '/Users/louisekirkham/Documents/my_projects/perch_vrp/data'
}

FILEPATHS = {
    'credentials': os.path.join(DIRECTORIES['data'], 'credentials.yml'),
    'delivery_points': os.path.join(DIRECTORIES['data'], '10_random_addresses.csv'),
    'dispatchers': os.path.join(DIRECTORIES['data'], 'dispatch_crew.csv'),
    'log': os.path.join(DIRECTORIES['data'], 'app.log'),
}


#!/usr/bin/env python
"""
PROJECT:
    Perch_VRP

CODE:
    config.py

SUMMARY:
    Configuration file for the codebase.

DOCS:
    None

DEPENDENCIES:
    None

LAST EDITED:
    2020-11-09  Created
    2020-04-03  Added RUN

CONTACT:
    Louise Kirkham <louisek@gmail.com.com>

REPO:
    https://github.com/LNKirkham/perch_vrp

"""

import yaml
from filepaths import FILEPATHS, local_api_key

RUN = {
    'INGEST_NEW_INPUTS': True,
    'DISTANCE_MATRIX': True,
    'ROUTING': True,
    'PLOT_SOLUTION': True,
}



API_KEY = yaml.load(open(local_api_key))
# API_KEY = credentials['api_key']
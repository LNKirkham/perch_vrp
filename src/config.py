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
    2020-11-09  Created - Louise

CONTACT:
    Louise Kirkham <louisek@gmail.com.com>

REPO:
    https://github.com/LNKirkham/perch_vrp

"""

import yaml
from filepaths import FILEPATHS

RUN = {
    'INGEST_NEW_INPUTS': False,
    'DISTANCE_MATRIX': True,
    'ROUTING': False,
    'PLOT_SOLUTION': False,
}


API_KEY = yaml.load(open('/Users/louisekirkham/Documents/personal/perch_vrp/data/credentials.yml'))
# API_KEY = credentials['api_key']
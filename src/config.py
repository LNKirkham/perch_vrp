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


with open(FILEPATHS['credentials']) as file:
    # The FullLoader parameter handles the conversion from YAML scalar values to Python the dictionary format
    credentials = yaml.load(file, Loader=yaml.FullLoader)

API_KEY = credentials['api_key']


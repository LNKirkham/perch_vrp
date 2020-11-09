#!/usr/bin/env python
"""
PROJECT:
    Perch_VRP

CODE:
    collection_point.py

SUMMARY:
    Contains the code to generate the collection point class

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

import pandas as pd


class CollectionPoint:
    '''This is a class for collection points'''

    def __init__(self, id_num, name, address, postcode, latitude, longitude):
        self.id_num = id_num
        self.name = name
        self.address = address
        self.postcode = postcode
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            'id_num': self.id_num,
            'name': self.name,
            'address': self.address,
            'postcode': self.postcode,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

# Initialise canababes with the CollectionPoint class
canababes = CollectionPoint('collect_01',
                            'Canababes',
                            'Unit 8 Hamlet Industrial Estate, 96 White Post Ln, London',
                            'E9 5EN',
                            '51.542540',
                            '-0.023000')

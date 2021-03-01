#!/usr/bin/env python
"""
PROJECT:
    Perch_VRP

CODE:
    main.py

SUMMARY:
    The main script of the Perch_VRP codebase

DOCS:
    None yet

DEPENDENCIES:
    Configuration parameters specified in config.py

RUNNING:
    $ python main.py

LAST EDITED:
    2020-11-09  Created - Louise

CONTACT:
    Louise Kirkham <louisek@gmail.com.com>

REPO:
    https://github.com/LNKirkham/perch_vrp

"""

import pandas as pd
from ingest_data import run_ingest_data
from distance_matrix import run_distance_matrix
from routing import run_routing
from filepaths import FILEPATHS
import logging
import logger_config
logger = logging.getLogger(__name__)


def main():

    logger.info('Running: main()')

    selected_locations_df, dispatch_crew_df = run_ingest_data(create_new=True)

    distance_matrix = run_distance_matrix(selected_locations_df, request_new=True)

    selected_locations_solution_df = run_routing(distance_matrix, dispatch_crew_df, selected_locations_df,
                                                 create_new=True)

    logger.info('Finished running main()')


if __name__ == '__main__':
    main()
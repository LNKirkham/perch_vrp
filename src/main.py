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
from filepaths import FILEPATHS
import logging
import logger_config
logger = logging.getLogger(__name__)


def main():

    logger.info('Running: main()')

    selected_locations_df = run_ingest_data(create_new=False)

    distance_matrix_df = run_distance_matrix(selected_locations_df, request_new=False)

    logger.info('Finished running main()')


if __name__ == '__main__':
    main()
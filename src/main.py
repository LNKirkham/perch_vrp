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
from src.config import RUN
from ingest_data import run_ingest_data
from distance_matrix import run_distance_matrix
from routing import run_routing
from filepaths import FILEPATHS
from collection_point import canababes
from plot_routing import plot_routing_solution
import logging
import logger_config
logger = logging.getLogger(__name__)


def main():

    logger.info('Running: main()')

    if RUN['INGEST_NEW_INPUTS']:
        logger.info('Creating new inputs')
        selected_locations_df, dispatch_crew_df, delivery_points_df = run_ingest_data()
    else:
        logger.info('Reading in inputs already created')
        selected_locations_df = pd.read_csv(FILEPATHS['selected_locations'], index_col=False)
        dispatch_crew_df = pd.read_csv(FILEPATHS['dispatchers'], index_col=False)

    if RUN['DISTANCE_MATRIX']:
        logger.info('Creating new distance matrix')
        distance_matrix = run_distance_matrix(selected_locations_df)
    else:
        logger.info('Reading in distance matrix already created')
        distance_matrix_df = pd.read_csv(FILEPATHS['distance_matrix'], index_col=False)
        # Convert to list of lists
        distance_matrix = distance_matrix_df.values.tolist()


    if RUN['ROUTING']:
        logger.info('Creating new inputs')
        selected_locations_solution_df = run_routing(distance_matrix, dispatch_crew_df, selected_locations_df)
    else:
        logger.info('Reading in inputs already created')
        selected_locations_solution_df = pd.read_csv(FILEPATHS['selected_locations_solution'], index_col=False)


    if RUN['PLOT_SOLUTION']:
        collection_point_df = pd.DataFrame.from_records([s.to_dict() for s in [canababes]])
        plot_routing_solution(delivery_points_df, collection_point_df, selected_locations_solution_df)


    logger.info('Finished running main()')


if __name__ == '__main__':
    main()
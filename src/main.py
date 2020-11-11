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
import numpy as np
import plotly.graph_objects as go
from distance_matrix import create_distance_matrix
from filepaths import FILEPATHS
from collection_point import canababes
import logging
logger = logging.getLogger(__name__)


def create_data(basic_locations_df):
    """Creates the data."""
    data = {}
    data['addresses'] = list(basic_locations_df['api_address'])
    return data



def prepare_ingested_data(collection_point_df, delivery_points_df, dispatch_crew_df):
    """Takes all the ingested inputs and prepares them for the distance matrix api"""

    # Concatenate all points into a single dataframe
    all_locations_df = pd.concat([collection_point_df, delivery_points_df, dispatch_crew_df]).reset_index(drop=True)

    # Add address for distance matrix api column
    all_locations_df['api_address'] = all_locations_df['address'] + ' ' + all_locations_df['postcode']
    all_locations_df['api_address'] = all_locations_df['api_address'].str.replace(',', '').str.replace(' ', '+')

    # Simplify problem, ignore dispatcher addresses for now:
    selected_locations_df = all_locations_df[~all_locations_df['id_num'].str.contains('dispatch')]

    return selected_locations_df


def ingest_inputs():
    """Gets the three data inputs as data frames: collection point, delivery points and dispatcher points"""

    logger.info('Ingesting inputs')

    # Read delivery points from csv
    delivery_points_df = pd.read_csv(FILEPATHS['delivery_points'], index_col=False)

    # Get collection point form collection point class module
    collection_point_df = pd.DataFrame.from_records([s.to_dict() for s in [canababes]])

    # Get dispatcher points from csv
    dispatch_crew_df = pd.read_csv(FILEPATHS['dispatchers'], index_col=False)

    return delivery_points_df, collection_point_df, dispatch_crew_df



def main():

    logger.info('Running main()')

    delivery_points_df, collection_point_df, dispatch_crew_df = ingest_inputs()

    selected_locations_df = prepare_ingested_data(collection_point_df, delivery_points_df, dispatch_crew_df)

    data = create_data(selected_locations_df)

    distance_matrix = create_distance_matrix(data)

    print(distance_matrix)

    distance_matrix_df = pd.DataFrame(distance_matrix)

    print(distance_matrix_df)

    distance_matrix_df.to_csv(FILEPATHS['distance_matrix'])

    logger.info('Finished running main()')

if __name__ == '__main__':
    # Main execution of the pipeline
    main()
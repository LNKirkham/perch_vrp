#!/usr/bin/env python
"""
PROJECT:
    Perch_VRP

CODE:
    ingest_data.py

SUMMARY:
    Ingests the input data

DOCS:
    None yet

DEPENDENCIES:
    Configuration parameters specified in config.py

LAST EDITED:
    2020-11-12  Created - Louise

CONTACT:
    Louise Kirkham <louisek@gmail.com.com>

REPO:
    https://github.com/LNKirkham/perch_vrp

"""

import pandas as pd
from collection_point import canababes
from filepaths import FILEPATHS
import src.column_names as cn
import logging
import logger_config
logger = logging.getLogger(__name__)


def prepare_ingested_data(collection_point_df, delivery_points_df, dispatch_crew_df):
    """
    Takes all the ingested inputs and prepares them for the distance matrix api.
    """

    logger.info('Running: prepare_ingested_data()')

    # Concatenate all points into a single dataframe
    all_locations_df = pd.concat([collection_point_df, delivery_points_df, dispatch_crew_df]).reset_index(drop=True)

    # Add address for distance matrix api column
    all_locations_df['api_address'] = all_locations_df['address'] + ' ' + all_locations_df['postcode']
    all_locations_df['api_address'] = all_locations_df['api_address'].str.replace(',', '').str.replace(' ', '+')

    # Simplify problem, ignore dispatcher addresses for now:
    selected_locations_df = all_locations_df[~all_locations_df['id_num'].str.contains('dispatch')]

    return selected_locations_df


def ingest_inputs():
    """
    Gets the three data inputs as data frames: collection point, delivery points and dispatcher points
    :return: three dataframes, one each for delivery points, colleciton points and dispatch points
    """

    logger.info('Running: ingest_inputs()')

    # Read delivery points from csv
    delivery_points_df = pd.read_csv(FILEPATHS['delivery_points'], index_col=False,
                                     dtype={cn.ID_NUM: 'str', cn.NAME: 'str', cn.ADDRESS: 'str', cn.POSTCODE: 'str',
                                            cn.LAT: 'float64', cn.LONG: 'float64'}
                                     )

    # Get collection point form collection point class module
    collection_point_df = pd.DataFrame.from_records([s.to_dict() for s in [canababes]])

    # Get dispatcher points from csv
    dispatch_crew_df = pd.read_csv(FILEPATHS['dispatchers'], index_col=False,
                                   dtype={cn.ID_NUM: 'str', cn.NAME: 'str', cn.ADDRESS: 'str', cn.POSTCODE: 'str',
                                          cn.LAT: 'float64', cn.LONG: 'float64'}
                                   )

    return delivery_points_df, collection_point_df, dispatch_crew_df


def run_ingest_data():

    logger.info('Running: run_ingest_data()')

    delivery_points_df, collection_point_df, dispatch_crew_df = ingest_inputs()
    selected_locations_df = prepare_ingested_data(collection_point_df, delivery_points_df, dispatch_crew_df)
    selected_locations_df.to_csv(FILEPATHS['selected_locations'], index=False)

    return selected_locations_df, dispatch_crew_df, delivery_points_df


if __name__ == '__main__':
    selected_locations_df, dispatch_crew_df, delivery_points_df = run_ingest_data()
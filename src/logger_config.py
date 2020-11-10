#!/usr/bin/env python
"""
PROJECT:
    Perch_VRP

CODE:
    logger_config.py

SUMMARY:
    This contains the configuration of the logger

DOCS:
    None yet

DEPENDENCIES:
    filepaths.py


LAST EDITED:
    2020-11-10  Created - Louise

CONTACT:
    Louise Kirkham <louisek@gmail.com.com>

REPO:
    https://github.com/LNKirkham/perch_vrp

"""
from filepaths import FILEPATHS
import logging
logger = logging.getLogger(__name__)


logging.basicConfig(
    level=logging.NOTSET,
    format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s',
    datefmt='%d-%b-%Y %H:%M:%S',
    handlers=[
        # logging.FileHandler(FILEPATHS['log']),  # Outputs to log file
        logging.StreamHandler()  # Outputs to terminal
    ]
)

# logger.info('1. Useful message')
# logger.error('2. Something bad happened')
# logger.debug('3. Debug message')
# logger.warning('4. This is a warning')
# logger.critical('5. Oh no, critical stuff')
# logger.exception('6. Exception message')
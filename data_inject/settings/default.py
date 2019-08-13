#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    settings.default
    ~~~~~~~~~~~~~~

    Module which contains all the configurations for Data inject.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

import logging
import os
from logging.config import dictConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE_PATH = os.path.join(BASE_DIR, 'logs/data_inject.log')
INPUT_DIR = '/home/pi/datalogger/input_data/'
PROCESSED_FILES_FOLDER = '/media/pi/USBDRIVE/'
DUMP_DIR = '/home/pi/datalogger/csv_dump/'
DYNAMO_DB = 'TestProd'
ROW_COUNT = 14999
# Log size in MB
LOG_SIZE = 5
# Log file back up count
BACKUP_COUNT = 5
config_dict = {
     'formatters': {
         'logger_level_msg':
             {
                'class': 'logging.Formatter', 'format': '[%(asctime)s] %(thread)d %(name)-10s %(module)-20s %'
                                                        '(levelname)-5s: %(lineno)d %(message)s'
             }
     },
     'handlers': {
         'h_stderr':
             {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'stream': 'ext://sys.stderr'
             },
         'file':
             {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_FILE_PATH,
                'formatter': 'logger_level_msg',
                'maxBytes': LOG_SIZE * 1024 * 1024,
                'backupCount': BACKUP_COUNT
             }
     },
     'root': {
         'handlers': ['h_stderr', 'file'], 'level': 'DEBUG'
     },
     'version': 1
}
logging.config.dictConfig(config_dict)


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
PROCESSED_FILES_FOLDER = '/home/pi/datalogger/processed_data/'
FAILED_FILES_FOLDER = '/home/pi/datalogger/failed_data/'

PUB_DUMP_DIR = '/home/pi/datalogger/csv_dump/'
SENT_DIR = '/home/pi/datalogger/mqtt_sent_dir/'
SUB_DUMP_DIR = '/home/pi/datalogger/csv_dump_sub/'


KAFKA_URL = "52.220.41.10:9092"
KAFKA_PORT = 9092
TOPIC = "cattle_iot_stream"

ROW_COUNT = 140
DHT_ROW_COUNT = 3

INFLUX_DB_HOST = "localhost"
INFLUX_DB_PORT = 8086
INFLUX_DB_USER = "root"
INFLUX_DB_PASSWORD = "root"
INFLUX_DB_NAME = "SENSOR_DATA"
INFLUX_DB_DHT_TABLE = 'acc_sensor_data_temp'
INFLUX_DB_ACC_TABLE = 'dht_sensor_data_temp'

DARK_SKY_API_URL = "https://api.darksky.net/forecast/"
LOCATION = "10.138955,76.483265"
SECRET_KEY = "453df98caa61e588e057985b19ed0d90"
UNIT = 'si'
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


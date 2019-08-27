#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    data_inject.monitor
    ~~~~~~~~~~~~~~

    Module which continuously watches the directory for new files and trigger injection when a new file is created.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import glob
import logging
import os
import shutil
import time
import pandas as pd
import influxdb
from random import randint
from settings.default import *
from influxdb import InfluxDBClient

import hex2dec_ble

dbClient = InfluxDBClient(INFLUX_DB_HOST, INFLUX_DB_PORT, INFLUX_DB_USER, INFLUX_DB_PASSWORD, INFLUX_DB_NAME)
batch_count = 10000
influx_pd = influxdb.DataFrameClient(INFLUX_DB_HOST, INFLUX_DB_PORT, INFLUX_DB_USER, INFLUX_DB_PASSWORD, INFLUX_DB_NAME, verify_ssl=False)


def move_processed_file(file, type):
    """
    Function to move the processed file to processed folder
    :param file:
    :return:
    """
    logging.info("moving the processed file: %s" % file)
    file_name_array = file.split(".")
    file_name = file_name_array[0]
    file_name = file_name+"_"+type+".csv"
    shutil.move(SUB_DUMP_DIR+file, PROCESSED_FILES_FOLDER+file_name)

def move_failed_file(file, type):
    """
    Function to move the failed file to failed folder
    :param file:
    :return:
    """
    logging.info("moving the failed file: %s" % file)
    file_name_array = file.split(".")
    file_name = file_name_array[0]
    file_name = file_name + "_" + type + ".csv"
    shutil.move(SUB_DUMP_DIR + file, FAILED_FILES_FOLDER + file_name)


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def splitDataFrameIntoSmaller(df, chunkSize = 10000):
    listOfDf = list()
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        listOfDf.append(df[i*chunkSize:(i+1)*chunkSize])
    return listOfDf


while 1:
    time.sleep(1)
    files = glob.glob(SUB_DUMP_DIR+'*.csv')
    for file in files:
        try:
            file_name = os.path.basename(file)
            file_name_array = file_name.split("_")
            last_item = file_name_array[-1]
            df = pd.read_csv(file)
            row_count = df.shape[0]
            print(row_count)
            if row_count == DHT_ROW_COUNT:

                logging.info("Watching the directory: %s for dht11 sensor  csv file having 2 rows in it" % SUB_DUMP_DIR)
                type = "DHT"
                df = pd.read_csv(file)
                df['time'] = df[' Timestamp'].apply(pd.to_datetime)
                df = df.set_index('time')
                for frame in splitDataFrameIntoSmaller(df):
                    influx_pd.write_points(frame, measurement="dht_sensor_data_final_tbl")
                move_processed_file(os.path.basename(file), type)

            elif row_count == ROW_COUNT:
                type = "ACC"
                logging.info("Watching the directory: %s for csv file having 15000 rows in it" % SUB_DUMP_DIR)
                processed_data = hex2dec_ble.process_file(file)
                processed_data.to_csv(file, index=False)
                df = pd.read_csv(file)
                df["time"] = df["Date"] + df["Time"]
                df['time'] = df['time'].apply(pd.to_datetime)
                df = df.set_index('time')
                for frame in splitDataFrameIntoSmaller(df):
                    influx_pd.write_points(frame, measurement='acc_sensor_data_final_tbl')
                move_processed_file(os.path.basename(file),type)
        except Exception as e:
            logging.info(e)
            logging.info("Mooving the failed file to %s" % FAILED_FILES_FOLDER)
            move_failed_file(os.path.basename(file), type)


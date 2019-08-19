#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    data_inject.readcsv
    ~~~~~~~~~~~~~~

    Module which reads the csv and inject the data into dyanamodb in batches.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

import csv
import os
import shutil
import boto3
from settings.default import *


def convert_csv_to_json_list(file):
    logging.info("Reading CSV file: %s and convert to json list" % file)
    items = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {}

            data['Index'] = row['Index']
            data['Date'] = row['Date']
            data['Time'] = row['Time']
            data['Data'] = row['Data']
            data['Timestamp'] = row['Timestamp']
            data['x'] = row['x']
            data['y'] = row['y']
            data['z'] = row['z']
            items.append(data)
        return items

def convert_dht11_csv_to_json_list(file):
    logging.info("Reading CSV file: %s and convert to json list" % file)
    items = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {}

            data['Index'] = row['Index']
            data['Timestamp'] = row[' Timestamp']
            data['Temperature *C'] = row[' Temperature *C']
            data['Humidity % '] = row[' Humidity % ']
            items.append(data)
        return items


def batch_write(items, sensor_type):
    logging.info("Injecting data into Dynamodb in batches")
    dynamodb = boto3.resource('dynamodb')

    if sensor_type ==1:
        db_name = DYNAMO_DB_DHT11
    else:
        db_name = DYNAMO_DB

    db = dynamodb.Table(db_name)
    with db.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)


def move_processed_file(file):
    """
    Function to move the processed file to processed folder
    :param file:
    :return:
    """
    logging.info("moving the processed file: %s" % file)
    shutil.move(INPUT_DIR+file, PROCESSED_FILES_FOLDER+file)


def main(files):
    for file in files:
        logging.info("Main function to convert csv to json list and batch inject data to dynamo db")

        file_name = os.path.basename(file)
        file_name_array = file_name.split("_")
        last_item = file_name_array[-1]
        file_path = INPUT_DIR + file

        if last_item == "DHT.csv":

            sensor_type = 1
            json_data = convert_dht11_csv_to_json_list(file_path)
        else:
            sensor_type = 2
            json_data = convert_csv_to_json_list(file_path)
        batch_write(json_data, sensor_type)
        move_processed_file(file)
    logging.info("Finished injecting data into Dynamodb.")


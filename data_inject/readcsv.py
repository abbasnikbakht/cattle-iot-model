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


def batch_write(items):
    logging.info("Injecting data into Dynamodb in batches")
    dynamodb = boto3.resource('dynamodb')
    db = dynamodb.Table(DYNAMO_DB)
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
        file_path = INPUT_DIR+file
        json_data = convert_csv_to_json_list(file_path)
        batch_write(json_data)
        move_processed_file(file)
    logging.info("Finished injecting data into Dynamodb.")


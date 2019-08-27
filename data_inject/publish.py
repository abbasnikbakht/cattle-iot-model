import logging
import shutil
import sys

import paho.mqtt.client as paho #mqtt library
import os
import json
import time
from datetime import datetime
from kafka import KafkaProducer
from json import dumps
from settings.default import *

producer = KafkaProducer(bootstrap_servers=[KAFKA_URL],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))


def on_publish(client,userdata,result): #create function for callback
    """
    call back function on publish
    :param client:
    :param userdata:
    :param result:
    :return:
    """
    print("published data is : ")
    print(result)


def move_processed_file(file):
    """
    Function to move the processed file to processed folder
    :param file:
    :return:
    """
    logging.info("moving the processed file: %s" % file)
    file_name = os.path.basename(file)
    shutil.move(PUB_DUMP_DIR+file, SENT_DIR+file_name)


def main(file):
    """
    Function which is used to publish the csv data to the topic
    :return:
    """

    logging.info("Connecting to Brocker")
    f = open(PUB_DUMP_DIR+file)
    imagestring = f.read()
    logging.info("Publishing message to the topic %s" % TOPIC)
    producer.send("TOPIC", value=imagestring)
    time.sleep(10)
    move_processed_file(file)


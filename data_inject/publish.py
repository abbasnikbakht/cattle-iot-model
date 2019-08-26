import logging
import shutil

import paho.mqtt.client as paho #mqtt library
import os
import json
import time
from datetime import datetime
from settings.default import *

broker=MQTT_BROCKER #host name , Replace with your IP address.
topic=TOPIC
port=MQTT_PORT #MQTT data listening port
client1= paho.Client("cattle_iot") #create client object

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
    client1.on_publish = on_publish  # assign function to callback
    client1.connect(broker, port, keepalive=60)  # establishing connection
    f = open(PUB_DUMP_DIR+file)
    file_content = f.read()
    byteArray = bytes(file_content, encoding='utf8')
    client1.publish(topic, byteArray, 0)
    move_processed_file(file)




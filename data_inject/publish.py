import shutil

import paho.mqtt.client as paho #mqtt library
import os
import json
import time
from datetime import datetime
from settings.default import *


broker="mqtt.eclipse.org" #host name , Replace with your IP address.
topic="test"
port=1883 #MQTT data listening port
client1= paho.Client("control1") #create client object

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
    shutil.move(INPUT_DIR+file, PROCESSED_FILES_FOLDER+file)


def main(file_list):
    """
    Function which is used to publish the csv data to the topic
    :return:
    """
    client1.on_publish = on_publish  # assign function to callback
    client1.connect(broker, port, keepalive=60)  # establishing connection
    for file in file_list:
        file_path = INPUT_DIR + file
        f = open(file_path)
        imagestring = f.read()
        print(imagestring)
        byteArray = bytes(imagestring, encoding='utf8')
        print(byteArray)
        client1.publish(topic, byteArray, 0)
        move_processed_file(file)




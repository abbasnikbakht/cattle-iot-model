import datetime
import json
import random
import shutil
from random import randint

import influxdb
import paho.mqtt.client as paho
from influxdb import InfluxDBClient
import pandas as pd
from settings.default import *

broker=MQTT_BROCKER #host name , Replace with your IP address.
topic = TOPIC # topic name
port=MQTT_PORT #MQTT data listening port


def move_processed_file(file):
    """
    Function to move the processed file to processed folder
    :param file:
    :return:
    """
    logging.info("moving the processed file: %s" % file)
    shutil.move(file, processed_folder+file)

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


def on_message(client, userdata, message):
    FileName = str("_".join(str(datetime.datetime.now()).split(" ")))
    FileName = str("_".join(FileName.split(":")))
    FileName = str("_".join(FileName.split(".")))
    FileName = str("_".join(FileName.split("-")))
    FileName = FileName + ".csv"
    print(message.payload)
    with open(SUB_DUMP_DIR+FileName, 'wb') as fd:
        fd.write(message.payload)

    # df = pd.read_csv(FileName)
    # print(df.head())
    # df['Index'] = [random.randint(1,10000000) for k in df.index]
    # for frame in splitDataFrameIntoSmaller(df):
    #     frame.set_index(pd.DatetimeIndex(frame['Index']), inplace=True)
    #     influx_pd.write_points(frame, measurement='acc_sensor_data_test_final')

    # move_processed_file(FileName)



client = paho.Client("cattle_iot_sub")  # create client object
client.on_message = on_message

print("connecting to broker host", broker)
client.connect(broker, port, keepalive=60)  # establishing connection
print("subscribing begins here")
client.subscribe(topic)  # subscribe topic test

while 1:
    client.loop_start()  # contineously checking for message

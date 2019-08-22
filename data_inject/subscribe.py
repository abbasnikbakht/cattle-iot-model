import json

import influxdb
import paho.mqtt.client as paho
from influxdb import InfluxDBClient
import pandas as pd

broker = "mqtt.eclipse.org"  # host name
topic = "test"  # topic name
dbClient = InfluxDBClient('localhost', 8086, 'root', 'root', 'SensorData')
batch_count = 10000
port=1883
influx_pd = influxdb.DataFrameClient('localhost', 8086, 'root', 'root', 'SensorData', verify_ssl=False)


def on_message(client, userdata, message):
    with open('test.csv', 'wb') as fd:
        fd.write(message.payload)

    for frame in pd.read_csv('test.csv', chunksize=batch_count):
        frame.set_index(pd.DatetimeIndex(frame['Index']), inplace=True)
        influx_pd.write_points(frame, measurement='test')


client = paho.Client("user")  # create client object
client.on_message = on_message

print("connecting to broker host", broker)
client.connect(broker, port)  # connection establishment with broker
print("subscribing begins here")
client.subscribe(topic)  # subscribe topic test

while 1:
    client.loop_start()  # contineously checking for message

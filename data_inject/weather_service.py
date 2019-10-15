import json
from time import sleep
import logging
import requests
from influxdb import InfluxDBClient
from settings.default import *

dbClient = InfluxDBClient(INFLUX_DB_HOST, INFLUX_DB_PORT, INFLUX_DB_USER, INFLUX_DB_PASSWORD, INFLUX_DB_NAME)

class RequestDarkSkyApi(object):
    """
    Class which request dark sky api and update the influx db with data
    """
    def __init__(self):
        """
        Inits RequestDarkSkyApi
        """
        self.request_url = DARK_SKY_API_URL+SECRET_KEY+"/"+LOCATION + "?units=" + UNIT


    def update_influx_db(self):
        """
        Function to insert data to influx db
        :return:
        """
        try:
            response = requests.get(self.request_url)
            new_str = response.content.decode('utf-8')  # Decode using the utf-8 encoding
            d = json.loads(new_str)
            response_data = d['currently']
            data = dict()
            data['temperature'] = response_data['temperature']
            humidity = response_data['humidity'] * 100

            data['humidity'] = humidity
            THI = (0.8 * response_data['temperature']) + (
                        response_data['humidity'] / 100 * (response_data['temperature'] - 14.4)) + 46.4
            data['THI'] = THI

            json_body = [
                {
                    "measurement": "dark_sky_api_data",
                    "time": int(str(response_data['time'])+'000000000'),
                    "fields": {
                        "THI": THI,
                        "humidity": humidity,
                        "temperature": response_data['temperature'],

                    }
                }
            ]

            return json_body
        except BaseException as e:
            logging.error(e)
            return None



while 1:
    sleep(300)
    obj = RequestDarkSkyApi()
    data = obj.update_influx_db()
    if data:
        logging.info("Inserting data into influx db")
        logging.info(data)
        dbClient.write_points(data)
        logging.info("inserted data")
    else:
        logging.info("No data recieved")

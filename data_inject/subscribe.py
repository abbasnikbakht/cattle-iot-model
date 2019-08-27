import datetime
import json
import shutil
from random import randint

from kafka import KafkaConsumer
from settings.default import *


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_URL],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))


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


def on_message(message):
    FileName = str("_".join(str(datetime.datetime.now()).split(" ")))
    FileName = str("_".join(FileName.split(":")))
    FileName = str("_".join(FileName.split(".")))
    FileName = str("_".join(FileName.split("-")))
    FileName = FileName + ".csv"

    message_str = message.value
    byteArray = bytes(message_str, encoding='utf8')

    with open(SUB_DUMP_DIR+FileName, 'wb') as fd:
        fd.write(byteArray)


while 1:
    logging.info("Consuming the message published from the topic %s" % TOPIC)
    for message in consumer:
        on_message(message)


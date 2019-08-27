#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    data_inject.file_processor
    ~~~~~~~~~~~~~~

    Module which continuously watches the directory for files which has 15000 rows in it.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import glob
import logging
import os
import shutil
import time
import pandas as pd
from settings.default import *
import hex2dec_ble
import publish

path_to_watch = PUB_DUMP_DIR

before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
    logging.info("Watching the directory: %s for new csv file" % path_to_watch)
    time.sleep (3)
    files = glob.glob(path_to_watch + '*.csv')

    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added:
        print("Added: ", ", ".join (added))
    for file in files:
        file_name = os.path.basename(file)
        file_name_array = file_name.split("_")
        last_item = file_name_array[-1]
        df = pd.read_csv(file)
        row_count = df.shape[0]

        if last_item == "DHT.csv":
            logging.info("Watching the directory: %s for dht11 sensor  csv file having 2 rows in it" % PUB_DUMP_DIR)
            if row_count == DHT_ROW_COUNT:
                publish.main(file_name)
                print("publish")
        else:
            logging.info("Watching the directory: %s for csv file having 15000 rows in it" % PUB_DUMP_DIR)
            if row_count == ROW_COUNT:
                publish.main(file_name)
                print("publish")
    # before = after

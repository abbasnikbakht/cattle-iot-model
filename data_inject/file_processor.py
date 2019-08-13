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
import os
import shutil
import time
import pandas as pd
from settings.default import *
import hex2dec_ble

def move_processed_file(file):
    """
    Function to move the processed file to processed folder
    :param file:
    :return:
    """
    logging.info("moving the file: %s to input directory" % file)
    shutil.move(DUMP_DIR+file, INPUT_DIR+file)


while 1:
    logging.info("Watching the directory: %s for csv file having 15000 rows in it" % DUMP_DIR)
    time.sleep (10)

    files = glob.glob(DUMP_DIR+'*.csv')
    for file in files:
        df = pd.read_csv(file)
        row_count = df.shape[0]
        print(row_count)
        if row_count == ROW_COUNT:
            processed_data = hex2dec_ble.process_file(file)
            processed_data.to_csv(file, index=False)
            move_processed_file(os.path.basename(file))


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    data_inject.monitor
    ~~~~~~~~~~~~~~

    Module which continuously watches the directory for new files and trigger injection when a new file is created.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

import time

import readcsv
import publish
from settings.default import *

path_to_watch = INPUT_DIR

before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
    logging.info("Watching the directory: %s for new csv file" % path_to_watch)
    time.sleep (3)
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added:
        print("Added: ", ", ".join (added))
        publish.main(added)
    before = after

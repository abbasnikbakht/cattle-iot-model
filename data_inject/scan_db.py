#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    data_inject.scan_db
    ~~~~~~~~~~~~~~

    Module which scans the dynamodb and convert the data into json.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from data_inject.settings.default import *


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_DB)


class DecimalEncoder(json.JSONEncoder):
    """
    Helper class to convert a DynamoDB item to JSON.

    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


response = table.scan()

for i in response['Items']:
    print(json.dumps(i, cls=DecimalEncoder))



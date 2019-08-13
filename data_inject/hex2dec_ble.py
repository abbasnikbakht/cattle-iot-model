#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np


pd.set_option('display.max_columns', None)


def spcrem(a):
    return a.split(' ')[1]


def tmstmp(a):
    return int(a[0:6], 16)*6.4/1000

def d1one(a):
    return int(a[6:10], 16)


def d2two(a):
    return int(a[10:14], 16)


def d3three(a):
    k = a[14:]
    while len(k) < 4:
        k = k+'0'
    return int(k, 16)

def conv(a):
    if a >> 15 == 1:
        a = -(65536-a)
    return a*(0.061/1000)


def process_file(file):
    """
    Function which process the csv file
    :param file:
    :return:
    """
    data = pd.read_csv(file)
    data = data.dropna()

    data[' Data '] = data[' Data '].apply(spcrem)

    z = [0] * (data.shape[0])
    i = 0

    while i <= data.shape[0]-1:
        if len(data[' Data '][i]) < 18 and (len(data[' Data '][i]) + len(data[' Data '][i + 1])) <= 18:
            z[i] = data[' Data '][i] + '0a' + data[' Data '][i + 1]
            i = i + 2

        else:
            z[i] = data[' Data '][i]
            i = i + 1

    data[' Data '] = z

    for i in range(data.shape[0]):
        if data[' Data '][i] == 0 or len(data[' Data '][i]) < 16:
            data = data.drop((data.Index[i] - 1), axis=0)

    TimeStamp = data[' Data '].apply(tmstmp)
    data = pd.concat([data, TimeStamp], axis=1)
    data.columns = ['Index', 'Date', 'Time', 'Data', 'Timestamp']
    d1 = data.Data.apply(d1one)
    d2 = data.Data.apply(d2two)
    d3 = data.Data.apply(d3three)

    data = pd.concat([data, d1, d2, d3], axis=1)
    data.columns = ['Index', 'Date', 'Time', 'Data', 'Timestamp', 'x', 'y', 'z']

    data.x = data.x.apply(conv)
    data.y = data.y.apply(conv)
    data.z = data.z.apply(conv)
    # print(data.head())
    return data

# file = 'csv_dump/test.csv'
# data_df = process_file(file)
# print(data_df)
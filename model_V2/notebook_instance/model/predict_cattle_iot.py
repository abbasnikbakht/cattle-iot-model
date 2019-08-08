#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pickle
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
with open('Kmeansmodel.pkl', 'rb') as inp:
    model = pickle.load(inp)


# In[23]:


start_timestamp = 495.68 #15:12:46
data = pd.read_csv('Cleandata_master.csv')
x_axis = data.x*9.8
y_axis = data.y*9.8
z_axis = data.z*9.8
#xi = [i for i in range(0, len(x))]

t = [i for i in range (0,len(data.Index))]

mag = np.sqrt(np.square(x_axis)+np.square(y_axis)+np.square(z_axis))
window = 2000
rolling_mean_x = x_axis.rolling(window).mean()
rolling_mean_y = y_axis.rolling(window).mean()
rolling_mean_z = z_axis.rolling(window).mean()

rolling_stdev_x = x_axis.rolling(window).std()
rolling_stdev_y = y_axis.rolling(window).std()
rolling_stdev_z = z_axis.rolling(window).std()

rolling_var_x = x_axis.rolling(window).var()
rolling_var_y = y_axis.rolling(window).var()
rolling_var_z = z_axis.rolling(window).var()

xtilt= np.arctan(rolling_mean_x/(np.sqrt(np.square(rolling_mean_y)+np.square(rolling_mean_z))))
xtilt = np.degrees(xtilt)
ytilt= np.arctan(rolling_mean_y/(np.sqrt(np.square(rolling_mean_x)+np.square(rolling_mean_z))))
ytilt = np.degrees(ytilt)
rolling_mean_mag = mag.rolling(window=1500).mean()

# print(rolling_mean_x,rolling_mean_y,rolling_mean_z)
data = pd.concat([rolling_mean_x,rolling_mean_y,rolling_mean_z],axis=1)


# In[ ]:





# In[2]:


data = data.dropna()
print(data.head())


# In[3]:


features = data.iloc[118000:120000,:]
print(features)
features.shape

# test_features.shape
predictions = model.predict(features)
print(predictions.tolist())


# In[ ]:





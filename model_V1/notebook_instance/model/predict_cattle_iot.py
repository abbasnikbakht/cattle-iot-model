#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pickle
import os
import json
import pandas as pd
with open('cattle_iot.pkl', 'rb') as inp:
    model = pickle.load(inp)


# In[23]:


test=pd.read_csv("test.csv")
test_features=test.iloc[1:10,0:3]
# test_features.shape
predictions = model.predict(test_features)
print(predictions)


# In[ ]:





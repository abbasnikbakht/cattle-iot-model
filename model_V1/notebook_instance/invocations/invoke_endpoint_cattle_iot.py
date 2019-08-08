#!/usr/bin/env python
# coding: utf-8

# In[21]:


import json

import boto3

sagemaker = boto3.client('sagemaker-runtime')
input_json = {"tBodyAcc-mean()-X":{"1":0.28602671},"tBodyAcc-mean()-Y":{"1":-0.013163359},"tBodyAcc-mean()-Z":{"1":-0.11908252}} 
input_json = json.dumps(input_json)


# In[22]:


def predict():
    # Get the json from the request
    # Send everything to the Sagemaker endpoint
    res = sagemaker.invoke_endpoint(
        EndpointName='cattle-iot-endpoint',
        Body=input_json,
        ContentType='application/json',
        Accept='Accept'
    )
    return res['Body'].read()


# In[23]:


data = predict()
print(data)


# In[ ]:





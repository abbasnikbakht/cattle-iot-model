# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

import os
import json
from sklearn.externals import joblib
import flask
import pandas as pd
from pandas import DataFrame
from flask import Flask, request, jsonify


#Define the path
prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

# Load the model components
model = joblib.load(os.path.join(model_path, 'cattle_iot.pkl'))

# The flask app for serving predictions
app = flask.Flask(__name__)
@app.route('/ping', methods=['GET'])
def ping():
    # Check if the classifier was loaded correctly
    try:
        model
        status = 200
    except:
        status = 400
    return flask.Response(response= json.dumps(' '), status=status, mimetype='application/json' )

@app.route('/invocations', methods=['POST'])
def transformation():
    data = flask.request.get_json()
    data_frame = convert_json(data)
    prediction = model.predict(data_frame)
    output = prediction.tolist()
    return jsonify(output)


def convert_json(data):
    df = DataFrame(data)
    return df


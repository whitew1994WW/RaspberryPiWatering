# web_app.py

from flask import Flask, render_template, make_response, jsonify
import pandas as pd
import json
from multiprocessing import Process
import plotly
import time
import plotly.express as px
import logging
from DataCollector import DataCollector

flask_app = Flask(__name__)


@flask_app.route('/')
def index():
    graphJSON = build_graph(pd.DataFrame({'Timestamp':[], 'Sensor':[]}))
    return render_template('Home.html', graphJSON=graphJSON)

# GET - data from sensor X
@flask_app.route('/get_data/<sensor>')
def get_data(sensor):
    sensor = sensor.replace("%20", " ")
    # CHeck it is a valid request
    logging.debug(f"API request STARTING for sensor {sensor}")
    if sensor not in DataCollector.get_sensors():
        raise NameError('Invaid sensor name')
    data_collector = DataCollector()
    df = data_collector.get_data(sensor)
    graphJson = build_graph(df)

    logging.debug(f"API request SUCCESSFUL for sensor {sensor}")
    logging.debug(f"GRAPH JSON looks like {graphJson}")
    return graphJson


# GET - list of active sensors
@flask_app.route('/get_sensors')
def get_sensors():
    sensors = DataCollector.get_sensors()
    return build_response(200, sensors)

# GET - Video Feed

# POST - Photo


def build_response(status, body):
    return jsonify(status=status, body=body)

def build_graph(df):
    fig = px.line(df, x='Timestamp', y='Sensor')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0')


# web_app.py

from flask import Flask, render_template, make_response, jsonify, Response
import pandas as pd
import json
from multiprocessing import Process
import plotly
import time
import plotly.express as px
import logging
from DataCollector import DataCollector
from flask import request
from VideoCamera import VideoCamera
import sys


logging.getLogger('boto').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.basicConfig(format='[{%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(filename='logs/flask.log'),
                        logging.StreamHandler(sys.stdout)
                    ],
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

flask_app = Flask(__name__)


selected_sensor = ""


@flask_app.route('/')
def index():
    graph_json = build_graph(pd.DataFrame({'Timestamp': [], 'Sensor': []}), "___", "___")
    return render_template('Home.html', graphJSON=graph_json)


# GET - data from sensor X
@flask_app.route('/get_data/<sensor>')
def get_data(sensor):
    sensor = sensor.replace("%20", " ")
    # CHeck it is a valid request
    logger.debug(f"API request STARTING for sensor {sensor}")
    if sensor not in DataCollector.get_sensors():
        raise NameError('Invaid sensor name')
    data_collector = DataCollector()
    unit = data_collector.sensors[sensor].get_unit()
    logger.debug(f"Unit fetched and is {unit}")
    df = data_collector.get_data(sensor)
    graph_json = build_graph(df, sensor, unit)

    logger.debug(f"API request SUCCESSFUL for sensor {sensor}")
    logger.debug(f"GRAPH JSON looks like {graph_json}")
    return graph_json


# GET - list of active sensors
@flask_app.route('/get_sensors')
def get_sensors():
    sensors = DataCollector.get_sensors()
    return build_response(200, sensors)


# Collect data and update the graph
@flask_app.route('/collect_data/<sensor>')
def collect_data(sensor):
    data_collector = DataCollector()
    data_collector.collect_data(0, 0)
    data_collector.save_current_data()
    graph_json = get_data(sensor)
    return graph_json


@flask_app.route('/video_feed')
def video_feed():
    pi_camera = VideoCamera(flip=False)  # Flip pi camera if upside down.
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# POST - Photo


def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        time.sleep(0.2)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def build_response(status, body):
    return jsonify(status=status, body=body)


def build_graph(df, sensor_name, unit):
    fig = px.line(df, x='Timestamp', y='Sensor', labels=dict(Timestamp="Reading Time", Sensor=sensor_name + f" /{unit}"))
    fig.update_yaxes(type='linear')
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    try:
        flask_app.run(debug=True, host='0.0.0.0')
    finally:
        shutdown_server()


# web_app.py

from flask import Flask, render_template, make_response, jsonify
import pandas as pd
import json
from multiprocessing import Process
import plotly
import time
import plotly.express as px
from DataCollector import DataCollector

flask_app = Flask(__name__)


@flask_app.route('/')
def index():
    df = pd.DataFrame({
      "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
      "Amount": [4, 1, 2, 2, 4, 5],
      "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
   })
    fig = px.bar(df, x="Fruit", y="Amount", color="City",    barmode="group")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('Home.html', graphJSON=graphJSON)

# GET - data from sensor X
@flask_app.route('/get_data/<sensor>')
def get_data(sensor):
    data_collector = DataCollector()
    data = data_collector.get_data(sensor)
    return build_response(200, data)


# GET - list of active sensors
@flask_app.route('/get_sensors')
def get_sensors():
    sensors = DataCollector.get_sensors()
    return build_response(200, sensors)

# GET - Video Feed

# POST - Photo


def build_response(status, body):
    return jsonify(status=status, body=body)


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0')

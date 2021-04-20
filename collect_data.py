from apscheduler.schedulers.background import BackgroundScheduler

from sensors.AHT20Temperature import AHT20Temperature
from sensors.AHT20Humidity import AHT20Humidity
import pandas as pd
import os
import credentials

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

frequency = {'minutes' : 10}
bucket = 's3://example-bucket-whitew1994'

sensors = {
    "Temperature": AHT20Temperature(),
    "Humidity": AHT20Humidity()
}


def start_data_collection():
    sched.start()
    sched.add_job(collect_data, 'interval', **frequency)


def stop_data_collection():
    sched.shutdown()


def collect_data():
    current_datetime = pd.Timestamp.now()
    for sensor_name in sensors.keys():
        df.loc[current_datetime, sensor_name] = sensors[sensor_name].get_reading()
    print(df.head())


def save_current_data(previous_day):
    bucket_file_name = bucket + '/year=' + str(previous_day.year) + '/month=' + str(previous_day.month) + '/' + \
                       str(previous_day.day) + '.csv'
    df.to_csv(bucket_file_name,
              index=True,
              storage_options={
                "key": AWS_ACCESS_KEY_ID,
                "secret": AWS_SECRET_ACCESS_KEY
                })
    print(bucket_file_name)


def create_empty_dataframe():
    new_df = pd.DataFrame(columns=sensors.keys())
    new_df.index.name = "Timestamp"
    return new_df


sched = BackgroundScheduler()
start_data_collection()
df = create_empty_dataframe()

previous_day = pd.Timestamp.now().date()
while 1:
    current_day = pd.Timestamp.now().date()
    # WHen it is a new day then save the results and create a new dataframe
    if current_day != previous_day:
        save_current_data(previous_day)
        previous_day = current_day
        df = create_empty_dataframe()









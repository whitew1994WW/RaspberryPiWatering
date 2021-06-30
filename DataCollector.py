from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import os
import logging

from sensors.AHT20Temperature import AHT20Temperature
from sensors.AHT20Humidity import AHT20Humidity
from sensors.GrowMoistureSensor import GrowMoistureSensor
from settings import settings
import credentials


# AWS credentials imported from credentials.py local file
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


class DataCollector:
    sensors = {
        "Temperature": AHT20Temperature(),
        "Humidity": AHT20Humidity(),
        "Soil Saturation": GrowMoistureSensor(settings['soil_moisture_sensor_pin'])
    }
    save_data = True

    def __init__(self, save_data=True, bucket='s3://example-bucket-whitew1994'):
        logging.debug("Setting up DataCollector class")
        self.sched = BackgroundScheduler()
        self.bucket = bucket
        self.save_data = save_data
        # Start the data collection at a regular interval
        self.df = self.create_empty_dataframe()

        # Start saving the data every day to S3
        self.sched.add_job(self.save_current_data, 'cron', hour='0')

    def collect_data(self, rain_rate, shower_volume):
        current_datetime = pd.Timestamp.now()
        logging.debug("Collecting Data at {}".format(current_datetime))
        self.df.loc[current_datetime, 'rain_rate'] = rain_rate
        self.df.loc[current_datetime, 'shower_volume'] = shower_volume
        for sensor_name in self.sensors.keys():
            self.df.loc[current_datetime, sensor_name] = self.sensors[sensor_name].get_reading()

    def save_current_data(self):
        previous_day = pd.Timestamp.now() - pd.Timedelta(1, unit='day')
        logging.debug("Saving data for day {}".format(previous_day))
        bucket_file_name = self.bucket + '/year=' + str(previous_day.year) + '/month=' + str(previous_day.month) + '/' + \
                           str(previous_day.day) + '.csv'
        self.df.to_csv(bucket_file_name,
                  index=False,
                  storage_options={
                    "key": AWS_ACCESS_KEY_ID,
                    "secret": AWS_SECRET_ACCESS_KEY
                    })
        print(bucket_file_name)
        self.df = self.create_empty_dataframe()

    def create_empty_dataframe(self):
        new_df = pd.DataFrame(columns=self.sensors.keys())
        new_df.index.name = "Timestamp"
        return new_df


if __name__ == '__main__':
    DataCollector()










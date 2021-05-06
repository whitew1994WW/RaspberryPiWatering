from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import os

from sensors.AHT20Temperature import AHT20Temperature
from sensors.AHT20Humidity import AHT20Humidity
from sensors.GrowMoistureSensor import GrowMoistureSensor

from RainSimulator import RainSimulator
import credentials


# AWS credentials imported from credentials.py local file
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


class CollectData:
    # Variables
    frequency = {'seconds': 10}
    bucket = 's3://example-bucket-whitew1994'
    water_sat_thresh = 20  # Water saturation level at which watering the plant starts
    pump_output_pin = 11

    # Rain options
    rain_time = 60  # minutes
    rain_amount = 200  # ml

    # Script options
    save_data_to_s3 = True
    water_when_low = True

    # Sensors for collecting data
    sensors = {
        "Temperature": AHT20Temperature(),
        "Humidity": AHT20Humidity(),
        "Soil Saturation": GrowMoistureSensor(18)
    }

    def __init__(self):
        self.sched = BackgroundScheduler()
        # Start the data collection at a regular interval
        self.df = self.create_empty_dataframe()
        self.start_data_collection()
        self.rain_sim = RainSimulator(trigger_saturation=self.water_sat_thresh, output_pin=self.pump_output_pin,
                                      time_to_rain=self.rain_time, volume_to_rain=self.rain_amount, calibrate=True)
        # Start saving the data every day to S3
        self.sched.add_job(self.save_current_data, 'cron', hour='0')

    def start_data_collection(self):
        self.sched.start()
        self.sched.add_job(self.collect_data, 'interval', **self.frequency)

    def stop_data_collection(self):
        self.sched.shutdown()

    def collect_data(self):
        current_datetime = pd.Timestamp.now()
        rain_rate = self.rain_sim.will_it_rain(self.df.loc[current_datetime, "Soil Saturation"])
        self.df.loc[current_datetime, 'rain_rate'] = rain_rate
        self.df.loc[current_datetime, 'rain_total_volume'] = self.rain_amount
        for sensor_name in self.sensors.keys():
            self.df.loc[current_datetime, sensor_name] = self.sensors[sensor_name].get_reading()

    def save_current_data(self):
        previous_day = pd.Timestamp.now() - pd.Timedelta(1, unit='day')
        bucket_file_name = self.bucket + '/year=' + str(previous_day.year) + '/month=' + str(previous_day.month) + '/' + \
                           str(previous_day.day) + '.csv'
        self.df.to_csv(bucket_file_name,
                  index=True,
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
    CollectData()










from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import logging
import boto3

from sensors.AHT20Temperature import AHT20Temperature
from sensors.AHT20Humidity import AHT20Humidity
from sensors.GrowMoistureSensor import GrowMoistureSensor
from sensors.BH1745Light import BH1745Light
from settings import settings
from credentials import *


# AWS credentials imported from credentials.py local file
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] =super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataCollector(metaclass=Singleton):
    sensors = {
        "Temperature": AHT20Temperature(),
        "Humidity": AHT20Humidity(),
        "Soil Saturation": GrowMoistureSensor(settings['soil_moisture_sensor_pin']),
        "Light Intensity": BH1745Light(mode='intensity'),
        "Red Light": BH1745Light(mode='red'),
        "Green Light": BH1745Light(mode='green'),
        "Blue Light": BH1745Light(mode='blue'),
    }
    additional_columns = ['rain_rate', 'shower_volume']
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
            reading = self.sensors[sensor_name].get_reading()
            self.df.loc[current_datetime, sensor_name] = self.sensors[sensor_name].get_reading()

    def save_current_data(self, previous_day=(pd.Timestamp.now() - pd.Timedelta(1, unit='day'))):
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
        new_df = pd.DataFrame(columns=list(self.sensors.keys()) + self.additional_columns)
        new_df.index.name = "Timestamp"
        return new_df

    def get_data(self, sensor):
        ac = boto3.client('athena', region_name='eu-west-2')
        query = f"""
        SELECT Timestamp, \"{sensor}\" FROM {settings["table_name"]} order by Timestamp
        """
        response = ac.start_query_execution(QueryString=query, QueryExecutionContext={'Database': settings["database_name"]}, ResultConfiguration={'OutputLocation': settings["output_location"]})
        state = ac.get_query_execution(QueryExecutionId=response['QueryExecutionId'])
        while not state['QueryExecution']['Status']['State'] == 'SUCCEEDED':
            state = ac.get_query_execution(QueryExecutionId=response['QueryExecutionId'])
            if state['QueryExecution']['Status']['State'] == 'FAILED':
                raise ConnectionError("Athena Query failed")
        result = ac.get_query_results(QueryExecutionId=response['QueryExecutionId'])
        rows = result['ResultSet']['Rows']
        timestamp_data = [pd.to_datetime(rows[i]['Data'][0]['VarCharValue']) for i in range(1, len(rows))]
        sensor_data = [rows[i]['Data'][1]['VarCharValue'] for i in range(1, len(rows))]
        df = pd.DataFrame()
        df['Timestamp'] = timestamp_data
        df['Sensor'] = sensor_data
        return df

    @staticmethod
    def get_sensors():
        return list(DataCollector.sensors.keys()) + DataCollector.additional_columns


if __name__ == '__main__':
    DataCollector()










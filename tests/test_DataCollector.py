import unittest

import pandas as pd

from DataCollector import DataCollector
import boto3
import random


class TestCollectData(unittest.TestCase):

    test_bucket = 'example-bucket-whitew1994'

    def setUp(self) -> None:
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(self.test_bucket)
        self.data_collector = DataCollector()


    # Delete contents of test bucket prior to testing
    def empty_bucket(self):
        bucket_versioning = self.s3.BucketVersioning(self.test_bucket)
        if bucket_versioning.status == 'Enabled':
            self.bucket.object_versions.delete()
        else:
            self.bucket.objects.all().delete()

    def test_collect_data(self):
        self.empty_bucket()
        rain_rate = random.randint(1, 100)
        self.data_collector.collect_data(rain_rate, 100)
        last_added = self.data_collector.df.iloc[-1:]
        print(last_added['rain_rate'].iloc[0])
        self.assertEqual(last_added['rain_rate'].iloc[0], rain_rate)
        self.assertIn('shower_volume', list(last_added.columns))
        self.assertIsNotNone(last_added['shower_volume'].iloc[0])

    def test_save_current_data(self):
        self.empty_bucket()
        sensors_rand_walk = {field: 50 for field in self.data_collector.get_sensors()}
        for day in range(5):
            test_data = {field: [] for field in self.data_collector.get_sensors()}
            test_data['Timestamp'] = []
            for minutes in range((24*60) // 10):
                test_data['Timestamp'].append(pd.Timestamp.now() + pd.Timedelta(day, unit='day') \
                                         + pd.Timedelta(minutes * 10, unit='minutes'))
                for sensor in sensors_rand_walk.keys():
                    sensors_rand_walk[sensor] = sensors_rand_walk[sensor] + random.randint(-5, 5)
                    sensors_rand_walk[sensor] = max(sensors_rand_walk[sensor], 0)

                    test_data[sensor].append(sensors_rand_walk[sensor])
            self.data_collector.df = pd.DataFrame(test_data)
            previous_day = pd.Timestamp.now() + pd.Timedelta(days=day)
            self.data_collector.save_current_data(previous_day=previous_day)

            bucket_file_name = 's3://' + self.test_bucket + '/year=' + str(previous_day.year) + '/month=' + str(previous_day.month) + '/' + \
                               str(previous_day.day) + '.csv'
        test_df = pd.read_csv(bucket_file_name)
        self.data_collector.df = pd.DataFrame(test_data)
        test_df_dict = test_df.to_dict()
        dc_dict = self.data_collector.df.to_dict()
        del test_df_dict['Timestamp'], dc_dict['Timestamp']
        self.assertEqual(test_df_dict, dc_dict)

    def test_get_data(self):
        sensor = "Temperature"
        df = self.data_collector.get_data(sensor)
        self.assertIsNotNone(df['Timestamp'].values)
        self.assertIsNotNone(df['Sensor'].values)
        self.assertGreater(len(df['Timestamp']), 1)
        self.assertGreater(len(df['Sensor']), 1)


if __name__ == '__main__':
    unittest.main()

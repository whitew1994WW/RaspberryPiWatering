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
        self.empty_bucket()

    def empty_bucket(self):
        bucket_versioning = self.s3.BucketVersioning(self.test_bucket)
        if bucket_versioning.status == 'Enabled':
            self.bucket.object_versions.delete()
        else:
            self.bucket.objects.all().delete()

    def test_collect_data(self):
        rain_rate = random.randint(1, 100)
        self.data_collector.collect_data(rain_rate)
        last_added = self.data_collector.df.iloc[-1:]
        print(last_added['rain_rate'].iloc[0])
        self.assertEqual(last_added['rain_rate'].iloc[0], rain_rate)
        self.assertIn('rain_total_volume', list(last_added.columns))
        self.assertIsNotNone(last_added['rain_total_volume'].iloc[0])

    def test_save_current_data(self):
        test_data = {'test_column': [1, 2, 3], 'test_column2': [1, 2, 3]}
        self.data_collector.df = pd.DataFrame(test_data)
        self.data_collector.save_current_data()
        previous_day = pd.Timestamp.now() - pd.Timedelta(1, unit='day')
        bucket_file_name = 's3://' + self.test_bucket + '/year=' + str(previous_day.year) + '/month=' + str(previous_day.month) + '/' + \
                           str(previous_day.day) + '.csv'
        test_df = pd.read_csv(bucket_file_name)
        self.assertEqual(test_df.to_dict(orient='list'), test_data)


if __name__ == '__main__':
    unittest.main()

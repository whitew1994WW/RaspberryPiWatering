import unittest
import logging
from sensors.BH1745Light import BH1745Light


class TestBH1745(unittest.TestCase):
    def setUp(self) -> None:
        self.sensor = BH1745Light()

    def test_check_sensor(self):
        logging.debug("Testing check_sensor()")
        self.assertEqual(self.sensor.check_sensor(), True)

    def test_get_reading(self):
        logging.debug(f"Testing get_reading()")
        reading = self.sensor.get_reading()
        logging.debug(f"Reading is {reading}")
        for key in reading.keys():
            logging.debug(f"Testing not None for reading[\'{key}\']")
            self.assertNotEqual(None, reading[key])



import unittest
import logging
from sensors.AHT20Temperature import AHT20Temperature


class TestAHT20Temperature(unittest.TestCase):
    def setUp(self) -> None:
        self.sensor = AHT20Temperature()

    def test_check_sensor(self):
        logging.debug("Testing check_sensor()")
        self.assertEqual(self.sensor.check_sensor(), True)

    def test_get_reading(self):
        logging.debug(f"Testing get_reading()")
        reading = self.sensor.get_reading()
        logging.debug(f'Humidity Sensor Reading: {reading} {self.sensor.get_unit()}')
        self.assertNotEqual(None, reading)



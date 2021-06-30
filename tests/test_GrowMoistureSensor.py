import unittest
import logging
from sensors.GrowMoistureSensor import GrowMoistureSensor


class TestGrowMoistureSensor(unittest.TestCase):
    def setUp(self) -> None:
        self.sensor = GrowMoistureSensor(18)

    def test_get_reading(self):
        logging.debug(f"Testing get_reading()")
        reading = self.sensor.get_reading()
        logging.debug(f'Moisture Sensor Reading: {reading} {self.sensor.get_unit()}')
        self.assertNotEqual(None, reading)

if __name__ == '__main__':
    unittest.main()





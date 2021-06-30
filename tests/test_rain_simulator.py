from unittest import TestCase
import unittest
from RainSimulator import RainSimulator
import logging
import RPi.GPIO as GPIO
from DataCollector import DataCollector
logging.getLogger().setLevel(logging.DEBUG)


class TestRainSimulator(TestCase):
    output_pin = 16
    # Ran before each test
    def setUp(self) -> None:
        self.rain_sim = RainSimulator(DataCollector(save_data=False), calibrate=False)

    def tearDown(self) -> None:
        self.rain_sim.stop_rain()

        GPIO.cleanup()

    def test_will_it_rain(self):
        self.rain_sim.is_raining = False
        self.rain_sim.minimum_days_between_rain = 0
        rain_rate = self.rain_sim.will_it_rain()
        self.rain_sim.stop_rain()
        state = GPIO.input(self.output_pin)
        self.assertIs(0, state)

        self.rain_sim.is_raining = True
        rain_rate = self.rain_sim.will_it_rain()
        state = GPIO.input(self.output_pin)
        self.assertIs(0, state)


    def test_shower(self):
        self.rain_sim.shower_count = self.rain_sim.NO_SHOWERS
        self.rain_sim.shower()
        out = input("Did the pump turn on y/n:\n")
        self.assertEqual(out, 'n')

        self.rain_sim.shower_count = 0
        self.rain_sim.shower()
        out = input("Did the pump turn on y/n:\n")
        self.assertEqual(out, 'y')

    def test_pump_water(self):
        self.rain_sim.pump_water()
        out = input("Did the pump turn on y/n:\n")
        self.assertEqual(out, 'y')

    def test_start_rain(self):
        self.rain_sim.start_rain()
        jobs = self.rain_sim.sched.get_jobs()
        self.assertEqual(len(jobs), 2)
        self.rain_sim.stop_rain()

if __name__ == '__main__':
    unittest.main()

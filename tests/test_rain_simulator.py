from unittest import TestCase
from RainSimulator import RainSimulator
import logging
import RPi.GPIO as GPIO

logging.getLogger().setLevel(logging.DEBUG)


class TestRainSimulator(TestCase):
    output_pin = 16
    # Ran before each test
    def setUp(self) -> None:
        self.rain_sim = RainSimulator(trigger_saturation=0, output_pin=self.output_pin, time_to_rain=10,
                                      volume_to_rain=100, calibrate=False)

    def tearDown(self) -> None:
        self.rain_sim.stop_rain()

        GPIO.cleanup()

    def test_will_it_rain(self):
        self.rain_sim.is_raining = False
        self.rain_sim.minimum_days_between_rain = 0
        rain_rate = self.rain_sim.will_it_rain(-1)
        self.rain_sim.stop_rain()
        state = GPIO.input(self.output_pin)
        self.assertIs(0, state)

        self.rain_sim.is_raining = True
        rain_rate = self.rain_sim.will_it_rain(-1)
        state = GPIO.input(self.output_pin)
        self.assertIs(0, state)

        self.rain_sim.is_raining = False
        rain_rate = self.rain_sim.will_it_rain(0)
        state = GPIO.input(self.output_pin)
        self.assertIs(0, state)
        self.assertIs(0, rain_rate)


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
        self.assertEqual(len(jobs), 1)
        self.rain_sim.stop_rain()


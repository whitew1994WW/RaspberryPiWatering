from unittest import TestCase
from RainSimulator import RainSimulator
import logging
import RPi.GPIO as GPIO

logging.getLogger().setLevel(logging.DEBUG)


class TestRainSimulator(TestCase):
    # Ran before each test
    def setUp(self) -> None:
        self.rain_sim = RainSimulator(trigger_saturation=0, output_pin=24, time_to_rain=10,
                                      volume_to_rain=100, calibrate=True)

    def tearDown(self) -> None:
        self.rain_sim.stop_rain()
        GPIO.cleanup()

    def test_will_it_rain(self):
        self.rain_sim.is_raining = False
        self.rain_sim.minimum_days_between_rain = 0
        self.fail()

    def test_shower(self):
        self.fail()

    def test_pump_water(self):
        self.fail()

    def test_turn_on_pump(self):
        self.rain_sim.turn_on_pump(5)

    def test_start_rain(self):
        self.fail()

    def test_calibrate(self):
        self.rain_sim.calibrate()

    def test_solve_linear_equation(self):
        self.fail()

    def test_water_vol_to_pump_time(self):
        self.fail()

    def test_save_calibration_settings(self):
        self.fail()

    def test_load_calibration_settings(self):
        self.fail()

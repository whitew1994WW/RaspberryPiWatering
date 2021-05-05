import time

import numpy as np
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import RPi.GPIO as GPIO


class RainSimulator:
    sched = None
    trigger_saturation = 0  # in % range: 0 - 100
    output_pin = 0
    rain_rate = 0  # in ml per minutes, how fast the pump will pump
    volume_to_rain = 0  # in ml, how much the pump will pump in one 'rain'
    time_to_rain = 0 # in minutes, how long the pump will pump in one 'rain'
    minimum_days_between_rain = 7 # in Days

    calibration_settings = {
        'warm_up_vol': 0, # in ml Volume of water in the tube of the pump
        'pump_rate': 0 # The rate the pump outputs water
    }

    TIME_BETWEEN_SHOWERS = 10  # in minutes, the short time period between successive "showers" as a part of one "rain"
    VOLUME_PER_SHOWER = 0  # in ml, the volume of water needed to rain every TIME_BETWEEN_SHOWERS to hit rain_rate
    NO_SHOWERS = 0  # Total number of showers per 'rain'
    shower_count = 0  # Number of showers completed so far in the 'rain'
    is_raining = False
    time_since_last_rain = datetime.now() - timedelta(days=minimum_days_between_rain)

    def __init__(self, trigger_saturation:int, output_pin:int, time_to_rain:float, volume_to_rain:float, calibrate=True):
        self.sched = BackgroundScheduler()
        self.trigger_saturation = trigger_saturation
        self.output_pin = output_pin
        self.time_to_rain = time_to_rain
        self.volume_to_rain = volume_to_rain
        self.rain_rate = volume_to_rain / time_to_rain
        self.NO_SHOWERS = self.time_to_rain / self.TIME_BETWEEN_SHOWERS
        self.VOLUME_PER_SHOWER = volume_to_rain / self.NO_SHOWERS

        # Set up the output pin (that turns on the pump
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.output_pin, GPIO.OUT)

        # If calibration is activated then perform the calibration and save the values locally
        if calibrate:
            self.calibrate()
        else:
            self.load_calibration_settings()

    def will_it_rain(self, saturation):
        """
        Checks if it should rain based on the saturation given and how recently it last rained.
        :return: Volume of water outputted by the pump
        """
        days_since_last_rain = (datetime.now() - self.time_since_last_rain).days
        if (saturation < self.trigger_saturation) & \
            (self.is_raining is False) & \
            (days_since_last_rain >= self.minimum_days_between_rain):
            self.start_rain()
            return self.volume_to_rain
        else:
            return 0

    def shower(self):
        """
        Performs one 'shower' of water of the plant
        """
        # If the number of showers completed in this 'rain' are equal to the maximum number of showers then stop the
        # 'rain' and reset the counter.
        if self.shower_count == self.NO_SHOWERS:
            self.stop_rain()
            self.shower_count = 0
        self.pump_water()
        self.shower_count += 1

    def pump_water(self, volume=0):
        """
        Pumps a fixed volume of water set in the VOLUME_PER_SHOWER or in the optional argument
        """
        if volume == 0:
            volume = self.VOLUME_PER_SHOWER

        pump_time = self.water_vol_to_pump_time(volume)
        self.turn_on_pump(pump_time)

    def turn_on_pump(self, time_active):
        """
        Turns on the pump for a fixed number of seconds
        :param time_active: In seconds the time the pump should be active for
        """
        GPIO.output(self.output_pin, 1)
        time.sleep(time_active)
        GPIO.output(self.output_pin, 0)

    def start_rain(self):
        self.time_since_last_rain = datetime.today()
        self.sched.start()
        self.sched.add_job(self.shower, 'interval', minutes=self.TIME_BETWEEN_SHOWERS)

    def stop_rain(self):
        self.sched.shutdown()

    def calibrate(self):
        calibrate_time = 30  # Seconds
        _ = input("Please fill up the tank with water and put the output nozzle into a measuring jug for calibration. "
                  "Press enter when ready.")
        self.turn_on_pump(30)
        _ = input("Please empty the water and press enter")
        self.turn_on_pump(30)
        total_volume_30 = input("Please enter the total volume of water outputted in ml:")
        _ = input("Please empty the water and press enter")
        calibrate_time = 60
        self.turn_on_pump(60)
        total_volume_60 = input("Please enter the total volume of water outputted in ml:")
        _ = input("Please empty the water and press enter")

        # Regression between time pump is active and the amount of water produced to estimate the warm up volume of the
        # pump - total_vol = rate*time - warm_up_vol (y = mx + c). This is solved with matricies
        # matricies AX = B where A = [[time_1, 1], [time_2, 1]] X = [rate, -warm_up_vol] and B = [[total_vol1],
        # [total_vol_2]]

        A = [[30, 1], [60, 1]]
        B = [[total_volume_30],[total_volume_60]]
        X = self.solve_linear_equation(A, B)

        self.calibration_settings['warm_up_vol'] = X[1][0]
        self.calibration_settings['pump_rate'] = X[0][0]
        self.save_calibration_settings()

    @staticmethod
    def solve_linear_equation(A, B):
        """
        Solves AX = B
        :return: X
        """
        A = np.array(A)
        B = np.array(B)
        X = np.linalg.inv(A).dot(B)
        return X

    def water_vol_to_pump_time(self, volume):
        """
        Uses the calibration settings in the below model for the pump to output the pump time:
        (total_vol + warm_up_vol) / pump_rate = pump_time
        :param volume: amount of water to calculate the water output for
        :return: pump_time, the time in seconds that the pump needs to be active to pump out 'volume' in ml of water
        """
        return (self.calibration_settings['warm_up_vol'] + volume) / self.calibration_settings['pump_rate']

    def save_calibration_settings(self):
        with open('calibration_settings.json', 'w') as f:
            json.dump(self.calibration_settings, f)

    def load_calibration_settings(self):
        with open('calibration_settings.json', 'r') as f:
            self.calibration_settings = json.load(f)

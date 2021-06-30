import time
import logging
import numpy as np
import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError
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

    def __init__(self, trigger_saturation: int, output_pin: int, time_to_rain: float,
                 volume_to_rain: float, calibrate=True):
        logging.debug("Setting up Class")
        self.sched = BackgroundScheduler()
        self.trigger_saturation = trigger_saturation
        self.output_pin = output_pin
        self.time_to_rain = time_to_rain
        self.volume_to_rain = volume_to_rain
        self.rain_rate = volume_to_rain / time_to_rain
        logging.info("Calculated rain rate is {}".format(self.rain_rate))
        self.NO_SHOWERS = self.time_to_rain / self.TIME_BETWEEN_SHOWERS
        logging.info("Calculated NO_SHOWERS is {}".format(self.NO_SHOWERS))
        self.VOLUME_PER_SHOWER = volume_to_rain / self.NO_SHOWERS
        logging.info("VOLUME_PER_SHOWER is {}".format(self.VOLUME_PER_SHOWER))

        logging.debug("Setting up the pinout")
        # Set up the output pin (that turns on the pump
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.output_pin, GPIO.OUT)

        # If calibration is activated then perform the calibration and save the values locally

        if calibrate:
            self.calibrate()
        else:
            self.load_calibration_settings()

    def will_it_rain(self, saturation):
        """
        Checks if it should rain based on the saturation given and how recently it last rained.
        :return: Rain rate currently
        """
        logging.debug("Running will_it_rain with {} input".format(saturation))
        days_since_last_rain = (datetime.now() - self.time_since_last_rain).days
        if (saturation < self.trigger_saturation) & \
            (self.is_raining is False) & \
            (days_since_last_rain >= self.minimum_days_between_rain):
            self.start_rain()
            return self.rain_rate
        elif self.is_raining:
            return self.rain_rate
        else:
            return 0


    def shower(self):
        """
        Performs one 'shower' of water of the plant
        """
        # If the number of showers completed in this 'rain' are equal to the maximum number of showers then stop the
        # 'rain' and reset the counter.
        logging.debug("Running shower()")
        logging.debug("Shower count is {}. NO_SHOWERS is {}".format(self.shower_count, self.NO_SHOWERS))
        if self.shower_count == self.NO_SHOWERS:

            self.stop_rain()
            self.shower_count = 0
            return None
        self.pump_water()
        self.shower_count += 1

    def pump_water(self, volume=0):
        """
        Pumps a fixed volume of water set in the VOLUME_PER_SHOWER or in the optional argument
        """
        logging.debug("Running pump_water() with {} volume".format(volume))
        if volume == 0:
            volume = self.VOLUME_PER_SHOWER

        pump_time = self.water_vol_to_pump_time(volume)
        self.turn_on_pump(pump_time)

    def turn_on_pump(self, time_active):
        """
        Turns on the pump for a fixed number of seconds
        :param time_active: In seconds the time the pump should be active for
        """
        logging.debug("Running turn_on_pump() with {} at pump {}".format(time_active, self.output_pin))
        GPIO.output(self.output_pin, GPIO.HIGH)
        time.sleep(time_active)
        GPIO.output(self.output_pin, GPIO.LOW)

    def start_rain(self):
        logging.debug("Starting 'rain'")
        self.time_since_last_rain = datetime.today()
        self.sched.start()
        self.sched.add_job(self.shower, 'interval', minutes=self.TIME_BETWEEN_SHOWERS)

    def stop_rain(self):
        logging.debug("Stopping 'rain'")
        GPIO.output(self.output_pin, GPIO.LOW)
        try:
            self.sched.shutdown()
        except SchedulerNotRunningError:
            logging.debug("Scheduler already stopped")

    def calibrate(self):
        logging.debug('Calibrating the pump')
        calibrate_time = 5
        calibrate_times = [calibrate_time, calibrate_time*2]
        total_vols = []
        _ = input("Please fill up the tank with water and put the output nozzle into a measuring jug for calibration. "
                  "Press enter when ready.")
        self.turn_on_pump(calibrate_time)
        _ = input("Please empty the water and press enter")
        for calibrate_time in calibrate_times:
            self.turn_on_pump(calibrate_time)
            total_vol = input("Please enter the total volume of water outputted in ml:")
            total_vols.append(float(total_vol))

        self.regression(total_vols, calibrate_times)

    def regression(self, total_vols, calibrate_times):
        #Not to overcomplicate things - estimate that the warm up volume and the rate - basic two point regression:
        diff = total_vols[1] - total_vols[0]

        self.calibration_settings['warm_up_vol'] = diff - total_vols[0]
        self.calibration_settings['pump_rate'] = diff / calibrate_times[0]
        self.save_calibration_settings()

    def water_vol_to_pump_time(self, volume):
        """
        Uses the calibration settings in the below model for the pump to output the pump time:
        (total_vol + warm_up_vol) / pump_rate = pump_time
        :param volume: amount of water to calculate the water output for
        :return: pump_time, the time in seconds that the pump needs to be active to pump out 'volume' in ml of water
        """
        pump_time = (self.calibration_settings['warm_up_vol'] + volume) / self.calibration_settings['pump_rate']
        logging.debug(f"Converting volume {volume} to pump_time {pump_time}")
        return pump_time

    def save_calibration_settings(self):
        logging.debug(f"Saving calibration_settings {self.calibration_settings}")
        with open('calibration_settings.json', 'w') as f:
            json.dump(self.calibration_settings, f)

    def load_calibration_settings(self):
        logging.debug(f"loading calibration settings {self.calibration_settings}")
        with open('calibration_settings.json', 'r') as f:
            self.calibration_settings = json.load(f)

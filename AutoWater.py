from DataCollector import DataCollector
from sensors.GrowMoistureSensor import GrowMoistureSensor
from apscheduler.schedulers.background import BackgroundScheduler
from RainSimulator import RainSimulator
import sys
import getopt
import logging


args = {'collect_data': None, 'host_data': None}

settings = {
    'water_sat_thresh': 20,  # Water saturation level at which watering the plant starts
    'pump_output_pin': 11,

    # Rain options
    'rain_time': 60,  # minutes
    'rain_amount': 200,  # ml
    'check_frequency': 40,  # In seconds

    # Script options
    'water_when_low': True,
    'calibrate': True}


def auto_water(collect_data=True, host_data=True):
    logging.debug('Starting the auto_water script')
    if collect_data:
        data_collector = DataCollector()
        soil_sensor = data_collector.sensors['Soil Saturation']
    else:
        data_collector = None
        soil_sensor = GrowMoistureSensor(DataCollector.soil_moisture_sensor_pin)

    sched = BackgroundScheduler()
    rain_sim = RainSimulator(trigger_saturation=settings['water_sat_thresh'], output_pin=settings['pump_output_pin'],
                             time_to_rain=settings['rain_time'], volume_to_rain=settings['rain_amount'], calibrate=settings['calibrate'])
    sched.add_job(check_rain, 'interval', [soil_sensor, rain_sim, data_collector], seconds=settings['check_frequency'])


def check_rain(soil_sensor, rain_sim, data_collector):
    logging.debug('Checking if it should rain.')
    rain_rate = rain_sim.will_it_rain(soil_sensor.get_reading())
    if data_collector:
        data_collector.data_collector(rain_rate)


if __name__ == '__main__':
    logging.debug("Main script started")
    try:
        opts, _ = getopt.getopt(sys.argv, "h", ["collect_data=", "host_data="])
    except getopt.GetoptError:
        print('AutoWater.py --collect_data=<bool> --host_data=<bool>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('AutoWater.py --collect_data=<bool> --host_data=<bool>')
            sys.exit()
        elif opt == '--collect_data':
            args['collect_data'] = arg
        elif opt == '--host_data':
            args['host_data'] = arg
        else:
            print('AutoWater.py --collect_data=<bool> --host_data=<bool>')
            sys.exit(2)
    logging.debug("Arguments parsed as {}".format(args))

    auto_water(**args)

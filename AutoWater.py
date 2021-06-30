from DataCollector import DataCollector
from RainSimulator import RainSimulator
from settings import settings
import sys
import getopt
import logging


args = {'save_data': None, 'host_data': None}


def auto_water(save_data=True, host_data=True, calibrate_pump=False):
    logging.debug('Starting the auto_water script')
    data_collector = DataCollector(save_data)
    rain_sim = RainSimulator(data_collector=data_collector)


def check_bool(arg):
    if arg not in ['False', 'True']:
        raise NameError("Invalid input argument. Only 'False' and 'True' are valid.")


if __name__ == '__main__':
    logging.debug("Main script started")
    try:
        opts, _ = getopt.getopt(sys.argv, "h", ["save_data=", "host_data=", "calibrate_pump="])
    except getopt.GetoptError:
        print('AutoWater.py --save_data=<True/False> --host_data=<True/False> --calibrate_pump=<True/False>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('AutoWater.py --save_data=<True/False> --host_data=<True/False> --calibrate_pump=<True/False>')
            sys.exit()
        elif opt == '--save_data':
            check_bool(arg)
            args['save_data'] = arg
        elif opt == '--host_data':
            args['host_data'] = arg
        elif opt == '--calibrate_pump':
            args['calibrate_pump'] = arg
        else:
            print('AutoWater.py --save_data=<True/False> --host_data=<True/False> --calibrate_pump=<True/False>')
            sys.exit(2)
    logging.debug("Arguments parsed as {}".format(args))

    auto_water(**args)


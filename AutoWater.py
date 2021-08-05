from DataCollector import DataCollector
from RainSimulator import RainSimulator
from settings import settings
import sys
import getopt
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[{%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(filename='logs/auto_water.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
args = {'save_data': None}


def auto_water(save_data=True, calibrate_pump=False):
    logger.debug('Starting the auto_water script')
    data_collector = DataCollector(save_data)
    rain_sim = RainSimulator(data_collector=data_collector)



def check_bool(arg):
    if arg not in ['False', 'True']:
        raise NameError("Invalid input argument. Only 'False' and 'True' are valid.")


if __name__ == '__main__':
    logger.debug("Main script started")
    try:
        opts, _ = getopt.getopt(sys.argv, "h", ["save_data=", "host_data=", "calibrate_pump="])
        logger.debug("Options passed on CMD line are {}".format(opts))
    except getopt.GetoptError:
        print('AutoWater.py --save_data=<True/False> --calibrate_pump=<True/False>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('AutoWater.py --save_data=<True/False> --calibrate_pump=<True/False>')
            sys.exit()
        elif opt == '--save_data':
            check_bool(arg)
            logger.debug("Save data arg is {}. As a bool is {}".format(arg, bool(arg)))
            args['save_data'] = arg
        elif opt == '--calibrate_pump':
            args['calibrate_pump'] = arg
        else:
            print('AutoWater.py --save_data=<True/False> --calibrate_pump=<True/False>')
            sys.exit(2)
    logger.debug("Arguments parsed as {}".format(args))

    auto_water(**args)



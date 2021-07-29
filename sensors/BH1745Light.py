#!/home/pi/Documents/main_dir/venv python
from sensors.AbstractSensor import AbstractSensor
import bh1745
import logging

logging.getLogger().setLevel(logging.DEBUG)



class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] =super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BH1745Wrapper(bh1745.BH1745, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BH1745Light(AbstractSensor):
    sensor_name = "BH1745"
    sensor_type = "Light"
    data_unit = "T"
    reading_default = {
        'red': None,
        'blue': None,
        'green': None,
        'intensity': None
    }

    def __init__(self, mode='intensity'):
        accepted_modes = ['intensity', 'red', 'green', 'blue']
        if mode not in accepted_modes:
            raise NameError(f"Mode must be in {accepted_modes}")
        self.mode = mode
        self.sensor = BH1745Wrapper(i2c_addr=0x39)
        self.sensor.setup()
        self.sensor.set_leds(1)

    def get_reading(self):
        reading = self.reading_default.copy()
        reading['red'], reading['green'], reading['blue'], reading['intensity'] = self.sensor.get_rgbc_raw()
        return reading[self.mode]

    def check_sensor(self):
        for i2c_addr in bh1745.I2C_ADDRESSES:
            try:
                self.sensor.setup(i2c_addr=i2c_addr)
                print('Found bh1745 on 0x{:02x}'.format(i2c_addr))
                return True
            except RuntimeError:
                pass

        if not self.sensor.ready():
            raise RuntimeError('No bh1745 found!')

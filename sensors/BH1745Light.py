#!/home/pi/Documents/auto_water/venv python
from sensors.AbstractSensor import AbstractSensor
import bh1745
import logging

logging.getLogger().setLevel(logging.DEBUG)


class BH1745Light(AbstractSensor):
    sensor_name = "BH1745"
    sensor_type = "Light"
    data_unit = "T"
    reading_default = {
        'r': None,
        'b': None,
        'g': None,
        'c': None
    }

    def __init__(self):
        self.sensor = bh1745.BH1745(i2c_addr=0x39)
        self.sensor.setup()
        self.sensor.set_leds(1)

    def get_reading(self):
        reading = self.reading_default.copy()
        reading['r'], reading['g'], reading['b'], reading['c'] = self.sensor.get_rgbc_raw()
        return reading

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

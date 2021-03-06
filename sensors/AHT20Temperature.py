from sensors.AbstractSensor import AbstractSensor
from sensor_aht20.AHT20 import AHT20

class AHT20Temperature(AbstractSensor):
    sensor_name = "AHT20"
    sensor_type = "Temperature"
    data_unit = "C"

    def __init__(self):
        # Initialize an AHT20
        self.aht20 = AHT20()

    def get_reading(self):
        temperature = self.aht20.get_temperature()
        return temperature

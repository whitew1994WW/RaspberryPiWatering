from sensors.AbstractSensor import AbstractSensor
import python_sensor_aht20.AHT20 as AHT20


class AHT20Temperature(AbstractSensor):
    sensor_name = "AHT20"
    sensor_type = "Temperature"
    data_unit = "T"

    def __init__(self):
        # Initialize an AHT20
        self.aht20 = AHT20.AHT20()

    def get_reading(self):
        temperature = self.aht20.get_temperature()
        return temperature

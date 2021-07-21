from sensors.AbstractSensor import AbstractSensor
from sensor_aht20.AHT20 import AHT20


class AHT20Humidity(AbstractSensor):
    sensor_name = "AHT20"
    sensor_type = "Humidity"
    data_unit = "% Air Water Saturation"

    def __init__(self):
        # Initialize an AHT20
        self.aht20 = AHT20()

    def get_reading(self):
        humidity = self.aht20.get_humidity()
        return humidity

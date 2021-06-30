import time
from sensors.AbstractSensor import AbstractSensor
from sensors.MeasurePWM import PulseSensorReader


class GrowMoistureSensor(AbstractSensor):
    sensor_name = "Grow Moisture"
    sensor_type = "Moisture"
    data_unit = "% Saturation"
    input_pin = 0
    min_frequency = 3   # Hz
    max_frequency = 27  # Hz

    def __init__(self, input_pin):
        self.input_pin = input_pin

    def get_reading(self):
        """
        Measures the frequency of the capacitive moisture sensor. The lower the frequency the more wet the soil.
        I have used the default values recommended by grow. Only a relative moisture
        sensitivity is important at this stage.
        :return: Percentage water saturation
        """
        reader = PulseSensorReader(self.input_pin)
        time.sleep(5)
        frequency = reader.get_frequency()
        reader.cancel()
        percent_saturation = self.calculate_percentage_saturation(frequency)
        return percent_saturation

    def calculate_percentage_saturation(self, frequency):
        if frequency > self.max_frequency:
            frequency = self.max_frequency
        elif frequency < self.min_frequency:
            frequency = self.min_frequency
        frequency_range = self.max_frequency - self.min_frequency
        relative_frequency = frequency - self.min_frequency
        percent_saturation = 100 * ((frequency_range - relative_frequency) / frequency_range)
        return percent_saturation

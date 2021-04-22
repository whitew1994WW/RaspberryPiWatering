import time
from sensors.AbstractSensor import AbstractSensor
from MeasurePWM import PulseSensorReader


class GrowMoistureSensor(AbstractSensor):
    sensor_name = "Grow Moisture"
    sensor_type = "Moisture"
    data_unit = "Arbitrary Saturation"
    input_pin = 0

    def __init__(self, input_pin):
        self.input_pin = input_pin

    def get_reading(self):
        reader = PulseSensorReader(self.input_pin)
        time.sleep(5)
        frequency = reader.get_frequency()
        pulse_width = reader.get_pulse_width()
        duty_cycle = reader.get_duty_cycle()
        reader.cancel()
        return frequency, pulse_width, duty_cycle




def test_sensor():
    sensor = GrowMoistureSensor(18)
    while True:
        print(sensor.get_reading())




test_sensor()

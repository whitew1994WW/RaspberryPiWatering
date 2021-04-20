import abc


class AbstractSensor(metaclass=abc.ABCMeta):
    sensor_name = ""
    sensor_type = ""
    data_unit = ""

    @abc.abstractmethod
    def get_reading(self):
        pass

    def get_unit(self):
        return self.data_unit

    def get_sensor_name(self):
        return self.sensor_name

    def get_sensor_type(self):
        return self.sensor_type

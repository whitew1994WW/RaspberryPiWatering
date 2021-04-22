import RPi.GPIO as GPIO
import time


class PulseSensorReader:
    def __init__(self, input_pin, weighting=0.0):
        self.input_pin = input_pin

        weighting = 0.0

        self._new = 1.0 - weighting  # Weighting for new reading.
        self._old = weighting  # Weighting for old reading.

        self._high_tick = None
        self._period = None
        self._high = None
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.input_pin, GPIO.IN)
        GPIO.add_event_detect(self.input_pin, GPIO.BOTH, self._cbf)

    def _cbf(self, channel):
        tick = time.time()
        level = GPIO.input(self.input_pin)
        if level == 1:
            if self._high_tick is not None:
                t = tick - self._high_tick

                if self._period is not None:
                    self._period = (self._old * self._period) + (self._new * t)
                else:
                    self._period = t

            self._high_tick = tick

        elif level == 0:

            if self._high_tick is not None:
                t = tick - self._high_tick

                if self._high is not None:
                    self._high = (self._old * self._high) + (self._new * t)
                else:
                    self._high = t

    def get_frequency(self):
        if self._period is not None:
            return 1000000.0 / self._period
        else:
            return 0.0

    def get_pulse_width(self):
        """
        PWM pulse width in microseconds.
        """
        if self._high is not None:
            return self._high
        else:
            return 0.0

    def get_duty_cycle(self):
        """
        PWM duty cycle percentage.
        """
        if self._high is not None:
            return 100.0 * self._high / self._period
        else:
            return 0.0

    def cancel(self):
        """
        Cancels the reader
        """
        GPIO.cleanup()



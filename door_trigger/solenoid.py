import time
from digitalio import DigitalInOut, Direction

class Solenoid:
    def __init__(self, solenoid_pin, open_duration=30):
        self.solenoid_pin = solenoid_pin
        self.open_duration = open_duration
        self._solenoid = DigitalInOut(self.solenoid_pin)
        self._solenoid.direction = Direction.OUTPUT
        self._solenoid.value = False
        self._opened_at = None

    def open(self):
        self._opened_at = time.time()
        self._solenoid.value = True

    def should_close(self):
        curr_time = time.time()
        return self.is_open() and ((self._opened_at + self.open_duration) <= curr_time)

    def is_open(self):
        return self._opened_at is not None

    def close(self):
        self._solenoid.value = False
        self._opened_at = None

    def close_if(self):
        if self.should_close():
            self.close()

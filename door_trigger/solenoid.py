import time
from adafruit_crickit import crickit
import sys
if sys.implementation.name == "cpython":
    import logging
if sys.implementation.name == "circuitpython":
    import adafruit_logging as logging

logger = logging.getLogger("Solenoid")
logger.setLevel(logging.INFO)

OPEN_FRACTION = 0.67
HOLD_OPEN_DELAY = 0.1
HOLD_OPEN_FRACTION = 0.5
DRIVE = {
    1: crickit.feather_drive_1,
    2: crickit.feather_drive_2,
    3: crickit.feather_drive_3,
    4: crickit.feather_drive_4,
}
class Solenoid:

    def __init__(self, drive, open_duration=30):
        drive = DRIVE[drive]
        drive.frequency = 1000
        drive.fraction = 0.0
        self.drive = drive
        self.open_duration = open_duration
        self._opened_at = None

    def open(self):
        logger.info("Solenoid.open")
        self._opened_at = time.time()
        # logger.info("   OPEN FRACTION GO")
        self.drive.fraction = OPEN_FRACTION
        time.sleep(HOLD_OPEN_DELAY)
        # logger.info("   HOLD OPEN FRACTION GO")
        self.drive.fraction = HOLD_OPEN_FRACTION


    def should_close(self):
        # logger.info("Solenoid.should_close")
        curr_time = time.time()
        return self.is_open() and ((self._opened_at + self.open_duration) <= curr_time)

    def is_open(self):
        # logger.info("Solenoid.is_open")
        return self._opened_at is not None

    def close(self):
        # logger.info("Solenoid.close")
        self.drive.fraction = 0.0
        self._opened_at = None

    def close_if(self):
        # logger.info("Solenoid.close_if")
        if self.should_close():
            self.close()

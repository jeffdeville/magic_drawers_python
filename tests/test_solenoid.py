import pytest
import time
from adafruit_crickit import crickit
from door_trigger.solenoid import Solenoid
from unittest.mock import MagicMock

def test_solenoid_init():
    crickit.drive_1.return_value = MagicMock()
    # board.D13.return_value = 101
    # mock = MagicMock()

    solenoid = Solenoid(crickit.drive_1)

    assert solenoid.drive == crickit.drive_1
    assert not solenoid.is_open()
    assert solenoid.open_duration == 30

    solenoid = Solenoid(crickit.drive_1, open_duration=60)

    assert solenoid.open_duration == 60



def test_open_close():
    crickit.drive_1.return_value = MagicMock()

    time.time = MagicMock(side_effect = [1,2,31,31])

    solenoid = Solenoid(crickit.drive_1)

    solenoid.open()
    assert solenoid.is_open()
    assert solenoid._opened_at == 1
    assert not solenoid.should_close()

    assert solenoid.should_close()
    solenoid.close_if()
    assert not solenoid.is_open()

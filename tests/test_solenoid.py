import pytest
import time
from adafruit_crickit import crickit
from door_trigger.solenoid import Solenoid
from unittest.mock import MagicMock

def test_solenoid_init():
    crickit.feather_drive_1.return_value = MagicMock()

    solenoid = Solenoid(1)

    assert solenoid.drive == crickit.feather_drive_1
    assert not solenoid.is_open()
    assert solenoid.open_duration == 30

    solenoid = Solenoid(1, open_duration=60)

    assert solenoid.open_duration == 60



def test_open_close():
    crickit.feather_drive_1.return_value = MagicMock()

    time.time = MagicMock(side_effect = [1,2,31,31])

    solenoid = Solenoid(1)

    solenoid.open()
    assert solenoid.is_open()
    assert solenoid._opened_at == 1
    assert not solenoid.should_close()

    assert solenoid.should_close()
    solenoid.close_if()
    assert not solenoid.is_open()

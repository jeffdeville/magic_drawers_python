import pytest
import time
import board
from door_trigger.solenoid import Solenoid
from unittest.mock import MagicMock

def test_solenoid_init():
    board.D13.return_value = 101

    solenoid = Solenoid(board.D13)

    assert solenoid.solenoid_pin == board.D13
    assert not solenoid.is_open()
    assert solenoid.open_duration == 30

    solenoid = Solenoid(board.D13, open_duration=60)

    assert solenoid.open_duration == 60



def test_open_close():
    board.D13.return_value = 101
    time.time = MagicMock(side_effect = [1,2,31,31])

    solenoid = Solenoid(board.D13)

    solenoid.open()
    assert solenoid.is_open()
    assert solenoid._opened_at == 1
    assert not solenoid.should_close()

    assert solenoid.should_close()
    solenoid.close_if()
    assert not solenoid.is_open()

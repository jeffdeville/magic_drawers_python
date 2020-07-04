import pytest
import adafruit_irremote
import board
from wand.irremote import IRRemote
from unittest.mock import MagicMock

def test_irremote_init():
    lock = MagicMock()

    remote = IRRemote(lock=lock, pin=board.A0)

    assert remote.lock == lock
    assert remote.decoder is not None

def test_irremote_check_code():
    lock = MagicMock()
    decoder = MagicMock()
    decoder.decode_bits.return_value = [1,2, 3, 4]
    adafruit_irremote.GenericDecode.return_value = decoder

    remote = IRRemote(lock=lock, pin=board.A0, ir_code=[1, 2, 3, 4])

    remote.check_code()
    lock.open.assert_called()

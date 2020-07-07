import pytest
from potions.scale_reader import ScaleReader
from potions.weight_scale_service import WeightScaleService, WeightScaleMeasurementValues
from unittest.mock import MagicMock, patch

def test_scale_reader_init():
    lock = MagicMock()
    scale_reader = ScaleReader(lock=lock, target_value=123.0, fudge_factor=10.0)
    assert scale_reader.lock == lock
    assert scale_reader.target_value == 123.0
    assert scale_reader.fudge_factor == 10.0
    assert scale_reader.consistent_measurements_before_stable == 2

    # defaults to a 10% fudge factor
    scale_reader = ScaleReader(lock=lock, target_value=123.0)
    assert scale_reader.fudge_factor == 12.3

# def test_scale_reader_check_when_connected():
#     scale_reader = ScaleReader(lock=MagicMock(), target_value=123.0)
#     mock_connection = MagicMock(connected=True)
#     scale_reader.ws_connection = mock_connection






def test_scale_reader_connected():
    scale_reader = ScaleReader(lock=MagicMock(), target_value=123.0)

    assert not scale_reader.connected()

    mock_connection = MagicMock(connected=False)
    scale_reader.ws_connection = mock_connection
    assert not scale_reader.connected()

    mock_connection = MagicMock(connected=True)
    scale_reader.ws_connection = mock_connection
    assert scale_reader.connected()


def test_scale_reader_get_measurement_when_not_connected():
    scale_reader = ScaleReader(lock=MagicMock(), target_value=123.0)
    assert scale_reader._get_measurement() is None

    mock_connection = MagicMock(connected=True)
    scale_reader.ws_connection = mock_connection
    assert scale_reader._get_measurement() is None


def test_scale_reader_get_measurement_when_connected():
    scale_reader = ScaleReader(lock=MagicMock(), target_value=123.0)
    mock_connection = MagicMock(connected=True) #, __getitem__=mock_service)

    mock_service = mock_connection.__getitem__.return_value
    mock_service.measurement_values = WeightScaleMeasurementValues(weight=14.1)
    scale_reader.ws_connection = mock_connection
    assert scale_reader._get_measurement() is None
    assert scale_reader.initial_value == 14.1


def test_scale_reader_scan():
    pass


def test_scale_reader_is_stable():
    scale_reader = ScaleReader(lock=MagicMock(), target_value=123.0)
    assert not scale_reader._is_stable()
    scale_reader.measurements.append(1)
    assert not scale_reader._is_stable()
    scale_reader.measurements.append(1)
    assert scale_reader._is_stable()
    scale_reader.measurements.append(2)
    assert not scale_reader._is_stable()


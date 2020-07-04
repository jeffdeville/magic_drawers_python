import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from .weight_scale_service import WeightScaleService

import platform;
if platform.python_implementation() == "CPython":
    from collections import deque
else:
    from ucollections import deque

class ScaleReader:
    def __init__(lock, target_value, fudge_factor, consistent_measurements_before_stable=2):
        self.lock = lock
        self.ble = adafruit_ble.BLERadio()
        self.ws_connection = None
        self.target_value = target_value
        # I want to retain the last N measurements, so that I can see whether
        # the weight measurements are stable or not.
        self.measurements = deque(maxlen=consistent_measurements_before_stable)
        self.consistent_measurements_before_stable = consistent_measurements_before_stable

        if fudge_factor is None:
            self.fudge_factor = target_value * 0.1
        else:
            self.fudge_factor = fudge_factor

    def check(self):
        if self.connected():
            measurement = _get_measurement()
            if self.target_value - fudge_factor <= measurement and \
                self.target_value + fudge_factor >= measurement:
                self.lock.open()
        elif self._scan():
            self.check()
        else:
            None

    def connected(self):
        return self.ws_connection and self.ws_connection.connected


    def _get_measurement(self):
        ws_service = self.ws_connection[WeightScaleService]
        if self.ws_connection.connected:
            measurement = ws_service.measurement_values

            if initial_value is None:
                self.initial_value = measurement

            self.measurements.append(measurement)
            if self._is_stable():
                return measurement

        return None


    def _scan(self):
        print("Scanning...")
        for adv in self.ble.start_scan(ProvideServicesAdvertisement, timeout=5):
            if WeightScaleService in adv.services:
                print("found a WeightScaleService advertisement")
                self.ws_connection = self.ble.connect(adv)
                print("Connected")
                break
        # Stop scanning whether or not we are connected.
        self.ble.stop_scan()
        print("Stopped _scan")


    def _is_stable(self):
        return sum(self.measurements) / self.consistent_measurements_before_stable == self.measurements[0]





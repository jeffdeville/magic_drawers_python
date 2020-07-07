import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from .weight_scale_service import WeightScaleService
from mycollections.deque import Deque

class ScaleReader:
    def __init__(self, lock, target_value, fudge_factor=None, consistent_measurements_before_stable=2):
        self.lock = lock
        self.ble = adafruit_ble.BLERadio()
        self.ws_connection = None
        self.target_value = target_value
        self.initial_value = None
        # I want to retain the last N measurements, so that I can see whether
        # the weight measurements are stable or not.
        self.measurements = Deque([], max_size=consistent_measurements_before_stable)
        self.consistent_measurements_before_stable = consistent_measurements_before_stable

        if fudge_factor is None:
            self.fudge_factor = target_value * 0.1
        else:
            self.fudge_factor = fudge_factor

    def check(self):
        if self.connected():
            weight = self._get_measurement()
            if weight is None:
                return None
            print("Weight: ")
            print(weight)
            if self.target_value - self.fudge_factor <= weight and \
                self.target_value + self.fudge_factor >= weight:
                # TODO: What do i need to do to make sure this does not just remain open constantly? The weight isn't going to go anyway...
                print("OPEN SESAME")
                self.lock.open()
        elif self._scan():
            # if scan returns true, it means the connection was established, so
            # should immediately start checking for values.
            self.check()
        else:
            None

    def connected(self):
        return self.ws_connection is not None and self.ws_connection.connected


    def _get_measurement(self):
        if not self.connected():
            return None

        # print("WS Connection--------------")
        # print(self.ws_connection)
        ws_service = self.ws_connection[WeightScaleService]
        # print("Weight Service--------------")
        # print(ws_service)
        # print("Weight Scale Measurement Values ------------")
        # print(ws_service.measurement_values)
        measurement_values = ws_service.measurement_values
        if measurement_values is None:
            return None
        weight = measurement_values.weight
        # print("Measurement Values--------------")
        # print(weight)
        # import pdb; pdb.set_trace()

        if self.initial_value is None:
            self.initial_value = weight

        self.measurements.append(weight)
        if self._is_stable():
            print("STABLE MEASUREMENT")
            return weight



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
        return self.connected()


    def _is_stable(self):
        if self.consistent_measurements_before_stable > len(self.measurements):
            return False
        return sum(self.measurements) / self.consistent_measurements_before_stable == self.measurements[0]





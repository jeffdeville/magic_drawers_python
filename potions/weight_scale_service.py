# The MIT License (MIT)
#
# Copyright (c) 2020 Dan Halbert for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`jeffdeville_ble_weight_scale`
================================================================================

BLE Weight Scale Service


* Author(s): Jeff Deville, altering Dan Halbert for Adafruit Industries Heart Rate Service

The Weight Scale Service is specified here:
https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Services/org.bluetooth.service.weight_scale.xml

Implementation Notes
--------------------

**Hardware:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's BLE library: https://github.com/adafruit/Adafruit_CircuitPython_BLE
"""
import struct
from collections import namedtuple

import _bleio
from adafruit_ble.services import Service
from adafruit_ble.uuid import StandardUUID
from adafruit_ble.characteristics import Characteristic, ComplexCharacteristic
from adafruit_ble.characteristics.int import Uint8Characteristic

__version__ = "0.0.0-auto.0"
# __repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE_Heart_Rate.git"

WeightScaleMeasurementValues = namedtuple(
  "WeightScaleMeasurementValues",
  ("weight", ),
)
"""Namedtuple for measurement values.

* `WeightScaleMeasurementValues.weight`

        Weight (float), in grams.

# For example::

#     weight = svc.measurement_values.weight
# """


class _WeightScaleMeasurement(ComplexCharacteristic):
    """Indicate-only characteristic of streaming weight scale data."""

    uuid = StandardUUID(0x2A9D)

    def __init__(self):
        super().__init__(properties=Characteristic.INDICATE)

    def bind(self, service):
        """Bind to a WeightScaleService."""
        bound_characteristic = super().bind(service)
        bound_characteristic.set_cccd(indicate=True)
        # Use a PacketBuffer that can store one packet to receive the WSM data.
        return _bleio.PacketBuffer(bound_characteristic, buffer_size=1)


class WeightScaleService(Service):
    """Service for reading from a Weight Scale."""

    # 0x180D is the standard HRM 16-bit, on top of standard base UUID
    uuid = StandardUUID(0x181D)

    # See WSP_V1.0.0.pdf in this repo, section 4.4
    # uint8: flags
    #  bit    0: Time Stamp Present if 1, missing if 0
    #  bit    1: Multiple Users Supported if 1. If 1, a User ID is present in Weight Measurement Characteristic
    #  bit    2: BMI and Height are present if 1, missing if 0
    #  NOT SURE WHAT TO DO WITH THESE, SO THEY ARE JUST 0
    #  bits 3-6: Weight Measurement Resolution - Measurement Units (bit 0) of the Weight Measurement characteristic
    #  bits 7-9: Height Measurement Resolution - Measurement Units (bit 0) of the Weight Measurement characteristic

    # next uint16: Weight Value
    #
    # Mandatory for Weight Scale Service
    weight_scale_measurement = _WeightScaleMeasurement()

    def __init__(self, service=None):
        super().__init__(service=service)
        # Defer creating buffer until needed.
        self._measurement_buf = None

    @property
    def measurement_values(self):
        """All the measurement values, returned as a WeightScaleMeasurementValues
        namedtuple.

        Return ``None`` if no packet has been read yet.
        """
        # print("Packet Size:")
        # print(self.weight_scale_measurement.packet_size)
        if self._measurement_buf is None:
            self._measurement_buf = bytearray(
                self.weight_scale_measurement.packet_size  # pylint: disable=no-member
            )
        buf = self._measurement_buf
        packet_length = self.weight_scale_measurement.readinto(  # pylint: disable=no-member
            buf
        )

        if packet_length == 0:
            # print("Packet Length == 0")
            return None
        # The flags are the 'features', which tell you where we want to go.
        next_byte = 1
        # <H = read an unsigned short (2 bytes) from the buffer,
        # starting at next_byte, which is 1 (after the feature byte)
        weight = struct.unpack_from("<H", buf, next_byte)[0]
        return WeightScaleMeasurementValues(weight)

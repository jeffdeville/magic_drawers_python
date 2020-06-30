Need to figure out how I want all the code organized.  There'll be:

code.py
potions
secret_knock
magnet
wand
door_trigger

code.py will wire these together, w/ regard to being where the pin configurations are managed. That info will be passed to the various code bits.

from potions import Potions
from secret_knock import SecretKnock
# Will handle waiting 30 seconds to relock
from door_trigger import configure_door
etc

potions_trigger = configure_door(soleniod_pin: D12, time_open: 30.0)
Potions.setup(trigger: potions_trigger, weight_min: 123.1, weight_max: 150.5, scale_delay: 10sec)

knock_trigger = configure_door(solenoid_pin: D13)
SecretKnock.setup(trigger: knock_trigger)
Magnet.setup(trigger: configure_door(solenoid_pin: D14))

while True:
  BLE.scan
  Potions.run
  SecretKnock.run




# Simple Solenoid Trigger
```
from time import sleep
from board import D13
from digitalio import DigitalInOut, Direction

solenoid = DigitalInOut(D13)
solenoid.direction = Direction.OUTPUT
solenoid.value = False

while True:
    solenoid.value = not solenoid.value
    sleep(2)
```

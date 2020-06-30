from time import sleep
from board import D13
from door_trigger import Solenoid


solenoid = Solenoid(D13)
solenoid.open()
while True:
    if solenoid.is_open():
        solenoid.close_if()
    else:
        solenoid.open()
    sleep(2)

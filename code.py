from time import sleep
from adafruit_crickit import crickit
from door_trigger.solenoid import Solenoid

def run():
    solenoid = Solenoid(crickit.feather_drive_1)
    print("running")

    while True:
        if solenoid.is_open():
            solenoid.close_if()
        else:
            solenoid.open()
        sleep(2)

if __name__ == '__main__':
    run()

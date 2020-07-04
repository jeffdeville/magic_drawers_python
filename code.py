from time import sleep
from door_trigger.solenoid import Solenoid

def run():
    solenoid = Solenoid(1)
    print("running")

    while True:
        if solenoid.is_open():
            solenoid.close_if()
        else:
            solenoid.open()
        sleep(2)

if __name__ == '__main__':
    run()

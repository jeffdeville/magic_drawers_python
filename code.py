from time import sleep
from board import D13
from door_trigger.solenoid import Solenoid

def run():
    solenoid = Solenoid(D13)
    solenoid.open()
    while True:
        if solenoid.is_open():
            solenoid.close_if()
        else:
            solenoid.open()
        sleep(2)

print("========================")
print("What does this say on the actual board?")
print(__name__)
print("========================")
if __name__ == '__main__':
    run()

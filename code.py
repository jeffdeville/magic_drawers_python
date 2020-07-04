from time import sleep
from door_trigger.solenoid import Solenoid
from wand.irremote import IRRemote
import board


def run():
    lock1 = Solenoid(1)
    irremote = IRRemote(lock=lock1, signal=board.A0)
    print("running")

    while True:
        lock1.close_if()
        irremote.check_code()
        sleep(2)

if __name__ == '__main__':
    run()

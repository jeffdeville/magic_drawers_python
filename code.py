from time import sleep
from door_trigger.solenoid import Solenoid
from wand.irremote import IRRemote
from potions.scale_reader import ScaleReader
import board


def run():
    lock1 = Solenoid(1)
    irremote = IRRemote(lock=lock1, signal=board.A0)

    lock2 = Solenoid(2)
    scale_reader = ScaleReader(lock=lock2, target_value=123.0, fudge_factor=10.0)

    print("running")

    while True:
        lock1.close_if()
        lock2.close_if()

        irremote.check()
        scale_reader.check()

        sleep(2)

if __name__ == '__main__':
    run()

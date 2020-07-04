import adafruit_irremote
import pulseio
import board


class IRRemote:
  def __init__(self, lock, signal=board.A0, ir_code=[223, 32, 239, 16]):
    self.lock = lock
    self.pulsein = pulseio.PulseIn(signal, maxlen=120, idle_state=True)
    self.decoder = adafruit_irremote.GenericDecode()
    self.ir_code = ir_code

  def check_code(self):
    # print("IRRemote.check_code")
    pulses = self.decoder.read_pulses(self.pulsein, blocking=False)
    if pulses is not None:
        try:
            # Attempt to convert received pulses into numbers
            received_code = self.decoder.decode_bits(pulses)
            print("NEC Infrared code received - yay - neato: ", received_code)
            if received_code == self.ir_code:
              self.lock.open()
        except adafruit_irremote.IRNECRepeatException:
            # We got an unusual short code, probably a 'repeat' signal
            # print("NEC repeat!")
            return
        except adafruit_irremote.IRDecodeException as e:
            # Something got distorted or maybe its not an NEC-type remote?
            # print("Failed to decode: ", e.args)
            return


#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md
#
# This code is for power management on a Raspberry Pi with GoPiGo3.
#
# GPIO 22 will be configured as input with pulldown. If pulled high, the RPi will halt.
#
# GPIO 23 needs to remain low impedance (output) set to a HIGH state. If GPIO 23 gets
# left floating (high impedance) the GoPiGo3 assumes the RPi has shut down fully.
# SW should never write GPIO 23 to LOW or set it as an INPUT.

import signal

class InterruptableRegion(object):
    def __init__(self, sig=(signal.SIGINT, signal.SIGTERM)):
        self.sig = sig
        self.interrupted = False
        self.released = False
        self.original_handler = {}

    def __enter__(self):
        self._validate_region_start()
        self._store_signal_default_handler()

        def _signal_invoked_new_handler(signum, frame):
            self._release()
            self.interrupted = True

        for sig in self.sig:
            signal.signal(sig, _signal_invoked_new_handler)

        return self

    def __exit__(self, type, value, tb):
        self._release()

    def _validate_region_start(self):
        if self.interrupted or self.released or self.original_handler:
            raise RuntimeError("An interruptable region can only be used once")

    def _release(self):
        if not self.released:
            self._reset_signal_default_handler()
            self.released = True

    def _store_signal_default_handler(self):
        for sig in self.sig:
            self.original_handler[sig] = signal.getsignal(sig)

    def _reset_signal_default_handler(self):
        for sig in self.sig:
            signal.signal(sig, self.original_handler[sig])

if __name__ == '__main__':

    with InterruptableRegion() as process:
        import RPi.GPIO as GPIO
        import time
        import os

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(23, GPIO.OUT)
        GPIO.output(23, True)

        while not process.interrupted:

            if GPIO.input(22):
                os.system('gopigo3 action stop')
                os.system('shutdown now -h')
            time.sleep(0.05)

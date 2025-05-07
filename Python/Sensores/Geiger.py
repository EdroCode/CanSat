from gpiozero import Button
from threading import Lock

class GeigerCounter:
    def __init__(self, pin=22):
        self.pin = pin
        self.pulse_count = 0
        self.lock = Lock()

        self.sensor = Button(self.pin, pull_up=False)
        self.sensor.when_pressed = self._count_pulse

    def _count_pulse(self):
        with self.lock:
            self.pulse_count += 1

    def read(self):
        with self.lock:
            count = self.pulse_count
            self.pulse_count = 0
            return count

    def reset(self):
        with self.lock:
            self.pulse_count = 0

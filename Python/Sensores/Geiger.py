from gpiozero import Button
import time
from threading import Lock

class GeigerCounter:
    def __init__(self, pin=22):
        self.pin = pin
        self.pulse_count = 0
        self.last_read_count = 0
        self.lock = Lock()

        self.sensor = Button(self.pin, pull_up=False)
        self.sensor.when_pressed = self._count_pulse

    def _count_pulse(self):
        with self.lock:
            self.pulse_count += 1

    def read(self):
        # Retorna o número de pulsos desde a última leitura
        with self.lock:
            delta = self.pulse_count - self.last_read_count
            self.last_read_count = self.pulse_count
        return delta

    def total(self):
        # Retorna o número total de contagens desde o início
        with self.lock:
            return self.pulse_count

    def reset(self):
        with self.lock:
            self.pulse_count = 0
            self.last_read_count = 0

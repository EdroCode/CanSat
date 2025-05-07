from gpiozero import Button
import time
from threading import Lock

class GeigerCounter:
    def __init__(self, pin=22):
        self.pin = pin
        self.pulse_count = 0
        self.start_time = time.time()
        self.lock = Lock()

        self.sensor = Button(self.pin, pull_up=False)
        self.sensor.when_pressed = self._count_pulse

    def _count_pulse(self):
        with self.lock:
            self.pulse_count += 1

    def read(self):
        #Retorna contagem por set time
        with self.lock:
            elapsed_time = time.time() - self.start_time
            cpm = (self.pulse_count / elapsed_time) * 60 if elapsed_time > 0 else 0
        return round(cpm, 2)

    def reset(self):
        with self.lock:
            self.pulse_count = 0
            self.start_time = time.time()


gc = GeigerCounter(pin=22)

while True:
    cpm = gc.read()
    print(f"Radiation: {cpm} CPM")
    time.sleep(2)  # read every 10 seconds

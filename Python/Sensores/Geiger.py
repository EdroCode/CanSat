import RPi.GPIO as GPIO
import time

PIN = 17  # Use the GPIO pin you connected OUT to

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

count = 0

def count_pulse(channel):
    global count
    count += 1
    print("Pulse detected! Total:", count)

GPIO.add_event_detect(PIN, GPIO.RISING, callback=count_pulse)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

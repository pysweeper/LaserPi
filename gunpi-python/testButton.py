import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)

def my_callback(pin):
    if GPIO.input(2):
        print("Rising.")
    else:
        print("Falling.")

GPIO.add_event_detect(2, GPIO.BOTH, callback=my_callback, bouncetime=20)

try:
    sleep(30)
    print("Times up")
finally:
    GPIO.cleanup()

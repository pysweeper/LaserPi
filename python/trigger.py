import os, datetime, time
import RPi.GPIO as GPIO
from subprocess import call

GPIO.setmode(GPIO.BCM)
TRIGGER=2
GPIO.setup(TRIGGER, GPIO.IN)

def shoot(pin):
    if GPIO.input(pin) == GPIO.LOW:
        print(str(datetime.datetime.now()), "Shot")
        call(["irsend","SEND_ONCE","laserpi","Shot02"])

def addTrigger():
    GPIO.add_event_detect(TRIGGER, GPIO.FALLING, callback=shoot, bouncetime=50)

def deleteTrigger():
    GPIO.remove_event_detect(TRIGGER)
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        addTrigger()
        while True:
            pass
    finally:
        deleteTrigger()


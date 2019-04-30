import unittest, sys, time, datetime
import threading
sys.path.append('../')
from connect import connect
from gun import Gun
from led import LED
from trigger import Trigger
import RPi.GPIO as GPIO

def main():
    '''
        Test LED
            Blink Red
            Solid Red
            Blink Green
            Solid Green
        Test Trigger
            Push trigger
            Hold trigger
        Test Send fake IR code
            Listen for callback
    '''
    led = LED()
    print("Testing LEDs.\n")
    eventOne = threading.Event()
    threadOne = threading.Thread(name='ledOnRed', target=setLED, args=(eventOne, 'red', led, 1))
    threadOne.start()
    answer = input("Is the Red LED on? y/n: ")
    eventOne.set()
    if not answer.lower() == 'y': return False
    eventTwo = threading.Event()
    threadTwo = threading.Thread(name='ledBlinkRed', target=toggleLED, args=(eventTwo, 'red', led, 1))
    threadTwo.start()
    answer = input("Is the Red LED blinking? y/n: ")
    # Get user input.
    eventTwo.set()
    if not answer.lower() == 'y': return False
    eventThree = threading.Event()
    threadThree = threading.Thread(name='ledOnGreen', target=setLED, args=(eventThree, 'green', led, 1))
    threadThree.start()
    answer = input("Is the Green LED on? y/n: ")
    eventThree.set()
    if not answer.lower() == 'y': return False
    eventFour = threading.Event()
    threadFour = threading.Thread(name='ledBlinkGreen', target=toggleLED, args=(eventFour, 'green', led, 1))
    threadFour.start()
    answer = input("Is the Green LED blinking? y/n: ")
    # Get user input.
    eventFour.set()
    if not answer.lower() == 'y': return False
    trigger = Trigger()
    print("Push and hold the trigger for 10 events.")
    i = 0
    while i < 10:
        if GPIO.input(trigger.TRIGGER) == GPIO.HIGH:
            time.sleep(0.1)
            print(("{}: Trigger detected.").format(datetime.datetime.now()))
            i += 1
    time.sleep(1)
    return True

def setLED(event, color, ledObject, t):
    ledObject.setLED(color, 'on')
    while not event.isSet():
        event_is_set = event.wait(t)
        if event_is_set:
            ledObject.setLED(color, 'off')
            #print("Exiting thread")

def toggleLED(event, color, ledObject, t):
    while not event.isSet():
        ledObject.toggleLED(color)
        event_is_set = event.wait(t)
        if event_is_set:
            ledObject.setLED(color, 'off')
            #print("Exiting thread")

if __name__ == "__main__":
    result = main()
    if result:
        print("Tests passed successfully.")
    else:
        print("Test failed.")

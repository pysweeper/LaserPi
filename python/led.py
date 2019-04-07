import datetime, time
import RPi.GPIO as GPIO


class LED():
    def __init__(self):
        self.RED=5
        self.GREEN=6
        self.REDstate = False
        self.GREENstate = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RED, GPIO.OUT)
        GPIO.setup(self.GREEN, GPIO.OUT)
        GPIO.output(self.RED, GPIO.LOW)
        GPIO.output(self.GREEN, GPIO.LOW)

    def setLED(self, color, state):
        color = self.RED if color == 'red' else self.GREEN
        state = GPIO.HIGH if state == 'on' else GPIO.LOW
        GPIO.output(color, state)

    def toggleLED(self, color):
        if color == 'red':
            if self.REDstate == False:
                self.REDstate = True
                GPIO.output(self.RED, GPIO.HIGH)
            else:
                self.REDstate = False
                GPIO.output(self.RED, GPIO.LOW)
        elif color == 'green':
            if self.GREENstate == False:
                self.GREENstate = True
                GPIO.output(self.GREEN, GPIO.HIGH)
            else:
                self.GREENstate = False
                GPIO.output(self.GREEN, GPIO.LOW)

if __name__ == "__main__":
    try:
        while True:
            led = LED()
            led.toggleLED('red')
            time.sleep(1)
            led.toggleLED('red')
            led.toggleLED('green')
            time.sleep(1)
            led.toggleLED('red')
            led.toggleLED('green')
            time.sleep(1)

    finally:
        GPIO.cleanup()

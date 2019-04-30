import datetime, time
import RPi.GPIO as GPIO


class LED():
    """ The LED class handles the LED functionality.
        Currently the LEDs only blink green if there
        is an active game and red if there is no active game.
    """
    def __init__(self):
        """ Constructor for the LED class
            Postconditions: The LEDs will be assigned green and red
            and states.
        """
        self.RED=5
        self.GREEN=6
        self.REDstate = False
        self.GREENstate = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.RED, GPIO.OUT)
        GPIO.setup(self.GREEN, GPIO.OUT)
        GPIO.output(self.RED, GPIO.LOW)
        GPIO.output(self.GREEN, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()

    def setLED(self, color, state):
        """ setLED
            Preconditions: The LED constructor has been called.
            Parameter color is a color that the LED will output.
            Parameter state represents the current game state.
            Postconditions: The LED will output red or green and high
            or low based on game state.
        """ 
        color = self.RED if color == 'red' else self.GREEN
        state = GPIO.HIGH if state == 'on' else GPIO.LOW
        GPIO.output(color, state)

    def toggleLED(self, color):
        """ toggleLED
            Preconditions: setLED has been called.
            Parameter color is a color that the LED will output.
            Postconditions: The led output will be updated.
        """
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
        led = LED()
        while True:
            led.toggleLED('red')
            led.toggleLED('green')
            time.sleep(1)

    finally:
        pass

import os, datetime, time
import RPi.GPIO as GPIO
from subprocess import call
from gun import Gun


class Trigger:
  """ The Trigger class handles all trigger events for the gun hardware.
      Establishing which gun has which id and username, "shooting" an 
      ir shot, and adding or deleting a trigger for event detection 
      (for a gun).
  """

  def __init__(self):
    """ Constructor for the Trigger class.
        Postconditions: The gunid and user name will be assigned to 
        a "gun" (to hardware).
    """
    self.TRIGGER=19
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.TRIGGER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    self.gun = Gun()
    self.gun.readIDFile()
    self.shotID = "Shot"+str(self.gun.id).zfill(2)

  def __del__(self):
    GPIO.remove_event_detect(self.TRIGGER)
    GPIO.cleanup()
  
  def shoot(self, pin):
    """ shoot
        Preconditions: The constructor has been called and a game has
        been started.
        Parameter pin is a GPIO input pin on the raspberry pi zero 
        board.
        Postconditions: A shot will be registered to the database
        via the fireShot definition in the gun class.
    """
    if GPIO.input(pin) == GPIO.HIGH:
      print(str(datetime.datetime.now()), "Shot")
      call(["irsend","SEND_ONCE","laserpi",self.shotID])
      self.gun.fireShot()
      return true
  
  def addTrigger(self):
    """ addTrigger
        Preconditions: The constructor has been called.
        Postconditions: Event detection for a trigger will be 
        established.
    """
    GPIO.add_event_detect(self.TRIGGER, GPIO.RISING, callback=self.shoot, bouncetime=50)
  
if __name__ == "__main__":
  try:
    trigger = Trigger()
    trigger.addTrigger()
    while True:
      pass
  finally:
    pass

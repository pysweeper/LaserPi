import os, datetime, time
import RPi.GPIO as GPIO
from subprocess import call
from gun import Gun


class Trigger:

  def __init__(self):
    self.TRIGGER=2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.TRIGGER, GPIO.IN)
    self.gun = Gun()
    self.gun.readIDFile()
    self.shotID = "Shot"+str(self.gun.id).zfill(2)
  
  def shoot(self, pin):
    if GPIO.input(pin) == GPIO.LOW:
      print(str(datetime.datetime.now()), "Shot")
      call(["irsend","SEND_ONCE","laserpi",self.shotID])
      self.gun.fireShot()
  
  def addTrigger(self):
    GPIO.add_event_detect(self.TRIGGER, GPIO.FALLING, callback=self.shoot, bouncetime=50)
  
  def deleteTrigger(self):
    GPIO.remove_event_detect(self.TRIGGER)
    GPIO.cleanup()
  
if __name__ == "__main__":
  try:
    trigger = Trigger()
    trigger.addTrigger()
    while True:
      pass
  finally:
    trigger.deleteTrigger()

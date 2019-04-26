#imports
import os, datetime, time
from gun import Gun
from trigger import Trigger
from led import LED
import lirc
from time import sleep

#prog defined in ~/.lircrc
prog="guns"

try:
  sockid = lirc.init(prog,blocking=False)
  trigger = Trigger()
  trigger.addTrigger()
  gun = Gun()
  led = LED()
  if (not gun.readIDFile()): quit()
  inGame = False
  while True:
    while not inGame:
      joined = gun.joinGame()
      if joined:
        inGame = True
      led.toggleLED('red')
      sleep(0.5)
    while inGame:
      led.toggleLED('green')
      led.setLED('red', 'off')
      code=lirc.nextcode()
      if code and code[0] != "Shot"+str(gun.id).zfill(2):
        #we got hit by something
        print(str(datetime.datetime.now()), "Got hit by " + str(code))
        gun.loseGame()
        led.setLED('red', 'on')
        led.setLED('green', 'off')
        inGame=False
      stillActive = gun.checkGame()
      if stillActive == False:
        inGame=False
        led.setLED('red', 'off')
        led.setLED('green', 'on')
      sleep(0.1)
  
finally:
  pass

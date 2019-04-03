#imports
from gun import Gun
from trigger import Trigger
import lirc
from time import sleep

#prog defined in ~/.lircrc
prog="guns"

try:
  sockid = lirc.init(prog,blocking=False)
  trigger = Trigger()
  trigger.addTrigger()
  gun = Gun()
  gun.readIDFile()
  inGame = True
  while True:
    while not inGame:
      joined = gun.joinGame()
      if joined:
        inGame = True
      sleep(0.1)
    while inGame:
      code=lirc.nextcode()
      if code and code[0] != "Shot"+str(gun.id).zfill(2):
        #we got hit by something
        print("Got hit by " + str(code))
        gun.loseGame()
        inGame=False
      sleep(0.1)
  
finally:
  trigger.deleteTrigger()

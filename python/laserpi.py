#imports
from gun import Gun
from trigger import Trigger
import lirc
from time import sleep

#prog defined in ~/.lircrc
prog="guns"

try:
  sockid = lirc.init(prog,blocking=False)
  #register trigers
  trigger = Trigger()
  trigger.addTrigger()
  #look for game
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
      #listen for hits
      code=lirc.nextcode()
      if code and code[0] != "Shot"+str(gun.id).zfill(2):
        #we got hit by something
        print("Got hit by " + str(code))
        gun.loseGame()
        inGame=False
      sleep(0.1)
  
finally:
  #clean up triggers.
  trigger.deleteTrigger()

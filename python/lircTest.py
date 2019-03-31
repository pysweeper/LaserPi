import lirc
from time import sleep

sockid = lirc.init("guns")

while True:
    sleep(0.1)
    code = lirc.nextcode()
    if code[0]=="Shot02":
        print("I shot myself")
    else:
        print("Player 1 shot me!")

lirc.deinit()

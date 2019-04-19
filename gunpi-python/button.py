from gpiozero import Button
import time

button = Button(2)

while True:
  if button.is_pressed:
    print("Button is pressed")
  else:
    print("Button is not pressed")

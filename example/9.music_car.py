#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from ezblock import __reset_mcu__
import time
__reset_mcu__()
time.sleep(0.01)
from picarx import set_dir_servo_angle
from picarx import dir_servo_angle_calibration
from Music import *
from ezblock import Pin
from ezblock import Ultrasonic
from picarx import forward
from ezblock import delay
from picarx import backward



Ref1 = None
distance = None
Ref2 = None

Ref1 = 30
Ref2 = 10
dir_servo_angle_calibration(0)
background_music('spry.mp3')

pin_D0=Pin("D0")

pin_D1=Pin("D1")


def forever():
  global Ref1, distance, Ref2
  distance = Ultrasonic(pin_D0, pin_D1).read()
  if distance >= Ref1:
    set_dir_servo_angle(0)
    forward(50)
  elif distance >= Ref2:
    set_dir_servo_angle(40)
    forward(50)
    delay(500)
  else:
    set_dir_servo_angle((-40))
    backward(50)
    delay(500)

if __name__ == "__main__":
    while True:
        forever()  
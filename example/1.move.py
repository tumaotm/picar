#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from ezblock import __reset_mcu__
import time
__reset_mcu__()
time.sleep(0.01)

from picarx import dir_servo_angle_calibration
from picarx import forward
from ezblock import delay
from picarx import backward
from picarx import set_dir_servo_angle
from picarx import stop


dir_servo_angle_calibration(0)
def forever():
  forward(50)
  delay(1000)
  backward(50)
  delay(1000)
  forward(50)
  set_dir_servo_angle((-30))
  delay(1000)
  forward(50)
  set_dir_servo_angle(30)
  delay(1000)
  set_dir_servo_angle(0)
  stop()
  delay(2000)

if __name__ == "__main__":
    while True:
        forever()  
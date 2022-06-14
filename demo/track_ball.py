from lib import Servo, PWM, Pin, ADC
import numpy as np
from vilib import Vilib
import time

PERIOD = 4095
PRESCALER = 10
TIMEOUT = 0.02

dir_servo_pin = Servo(PWM('P2'))
camera_servo_pin1 = Servo(PWM('P0'))
camera_servo_pin2 = Servo(PWM('P1'))
left_rear_pwm_pin = PWM("P13")
right_rear_pwm_pin = PWM("P12")
left_rear_dir_pin = Pin("D4")
right_rear_dir_pin = Pin("D5")

S0 = ADC('A0')
S1 = ADC('A1')
S2 = ADC('A2')

Servo_dir_flag = 1
dir_cal_value = 0
cam_cal_value_1 = 0
cam_cal_value_2 = 0
motor_direction_pins = [left_rear_dir_pin, right_rear_dir_pin]
motor_speed_pins = [left_rear_pwm_pin, right_rear_pwm_pin]
cali_dir_value = [-1, 1]
cali_speed_value = [0, 0]
# 初始化PWM引脚
for pin in motor_speed_pins:
    pin.period(PERIOD)
    pin.prescaler(PRESCALER)


def set_motor_speed(motor, speed):
    global cali_speed_value, cali_dir_value
    motor -= 1
    if speed >= 0:
        direction = 1 * cali_dir_value[motor]
    elif speed < 0:
        direction = -1 * cali_dir_value[motor]
    speed = abs(speed)
    if speed != 0:
        speed = int(speed / 2) + 50
    speed = speed - cali_speed_value[motor]
    if direction < 0:
        motor_direction_pins[motor].high()
        motor_speed_pins[motor].pulse_width_percent(speed)
    else:
        motor_direction_pins[motor].low()
        motor_speed_pins[motor].pulse_width_percent(speed)


def motor_speed_calibration(value):
    global cali_speed_value, cali_dir_value
    cali_speed_value = value
    if value < 0:
        cali_speed_value[0] = 0
        cali_speed_value[1] = abs(cali_speed_value)
    else:
        cali_speed_value[0] = abs(cali_speed_value)
        cali_speed_value[1] = 0


def motor_direction_calibration(motor, value):
    # 0: positive direction
    # 1:negative direction
    global cali_dir_value
    motor -= 1
    if value == 1:
        cali_dir_value[motor] = -1*cali_dir_value[motor]


def dir_servo_angle_calibration(value):
    global dir_cal_value
    dir_cal_value = value
    dir_servo_pin.angle(dir_cal_value)


def set_dir_servo_angle(value):
    global dir_cal_value
    value = round(value)
    # print("set_dir_servo_angle:%s"%value)
    dir_servo_pin.angle(value+dir_cal_value)


def camera_servo1_angle_calibration(value):
    global cam_cal_value_1
    cam_cal_value_1 = value
    camera_servo_pin1.angle(cam_cal_value_1)


def camera_servo2_angle_calibration(value):
    global cam_cal_value_2
    cam_cal_value_2 = value
    camera_servo_pin2.angle(cam_cal_value_2)


def set_camera_servo1_angle(value):
    global cam_cal_value_1
    camera_servo_pin1.angle(value+cam_cal_value_1)


def set_camera_servo2_angle(value):
    global cam_cal_value_2
    camera_servo_pin2.angle(value+cam_cal_value_2)


def get_adc_value():
    adc_value_list = []
    adc_value_list.append(S0.read())
    adc_value_list.append(S1.read())
    adc_value_list.append(S2.read())
    return adc_value_list


def set_power(speed):
    set_motor_speed(1, speed)
    set_motor_speed(2, speed)


def backward(speed):
    set_motor_speed(1, -1*speed)
    set_motor_speed(2, -1*speed)


def forward(speed):
    set_motor_speed(1, speed)
    set_motor_speed(2, speed)


def stop():
    set_motor_speed(1, 0)
    set_motor_speed(2, 0)


def color_follow():
    global pan_angle_color, tilt_angle_color
    Vilib.color_detect_switch(True)
    status = [Vilib.color_detect_object('x'), Vilib.color_detect_object('y')]
    size = [Vilib.color_detect_object(
        'width'), Vilib.color_detect_object('height')]
    time.sleep(0.005)
    # on left -1 on right 1
    if status[0] == -1:
        pan_angle_color = pan_angle_color + 1
        set_camera_servo1_angle(min(90, pan_angle_color))
        set_dir_servo_angle(max(-45, -pan_angle_color))
    elif status[0] == 1:
        pan_angle_color = pan_angle_color - 1
        set_camera_servo1_angle(max(-90, pan_angle_color))
        set_dir_servo_angle(min(45, -pan_angle_color))
    if status[1] == -1:
        tilt_angle_color = tilt_angle_color + 1
        set_camera_servo2_angle(min(45, tilt_angle_color))
    elif status[1] == 1:
        tilt_angle_color = tilt_angle_color - 1
        set_camera_servo2_angle(max(-45, tilt_angle_color))
    elif 0 < size[0] < 100 or 0 < size[1] < 100:
        forward(50)
    else:
        stop()
    # print(size)


Vilib.camera_start()
Vilib.detect_color_name('yellow')
pan_angle_color = 0
tilt_angle_color = 0
color_follow()

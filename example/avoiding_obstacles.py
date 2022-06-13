from picarx import Picarx
import time


def main():
    try:
        px = Picarx()
        # px = Picarx(ultrasonic_pins=['D2','D3']) # tring, echo
        px.forward(10)
        while True:
            distance = px.ultrasonic.read()
            print("distance: ", distance)
            if distance > 0 and distance < 300:
                if distance < 25:
                    px.set_dir_servo_angle(-35)
                else:
                    px.set_dir_servo_angle(0)

            time.sleep(0.5)
            for angle in range(0, 35):
                px.set_dir_servo_angle(angle)
                time.sleep(0.01)
            for angle in range(35, -35, -1):
                px.set_dir_servo_angle(angle)
                time.sleep(0.01)
            for angle in range(-35, 0):
                px.set_dir_servo_angle(angle)
                time.sleep(0.01)
            px.forward(0)
            time.sleep(1)
    
            for angle in range(0, 35):
                px.set_camera_servo1_angle(angle)
                time.sleep(0.01)
            for angle in range(35, -35, -1):
                px.set_camera_servo1_angle(angle)
                time.sleep(0.01)
            for angle in range(-35, 0):
                px.set_camera_servo1_angle(angle)
                time.sleep(0.01)
            for angle in range(0, 35):
                px.set_camera_servo2_angle(angle)
                time.sleep(0.01)
            for angle in range(35, -35, -1):
                px.set_camera_servo2_angle(angle)
                time.sleep(0.01)
            for angle in range(-35, 0):
                px.set_camera_servo2_angle(angle)
                time.sleep(0.01)
    

    finally:
        px.forward(0)


if __name__ == "__main__":
    main()

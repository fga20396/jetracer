import pygame
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT

# Initialize Motor HAT
mh = Adafruit_MotorHAT(addr=0x60)
left_motor = mh.getMotor(1)
right_motor = mh.getMotor(2)

# Dead zone threshold
DEAD_ZONE = 0.1

def apply_dead_zone(value, threshold=DEAD_ZONE):
    return value if abs(value) > threshold else 0.0

def set_motor_speed(motor, speed):
    speed = max(min(int(speed * 255), 255), -255)
    if speed > 0:
        motor.run(Adafruit_MotorHAT.FORWARD)
        motor.setSpeed(speed)
    elif speed < 0:
        motor.run(Adafruit_MotorHAT.BACKWARD)
        motor.setSpeed(-speed)
    else:
        motor.run(Adafruit_MotorHAT.RELEASE)

def stop_motors():
    left_motor.run(Adafruit_MotorHAT.RELEASE)
    right_motor.run(Adafruit_MotorHAT.RELEASE)

# Initialize Pygame and Joystick
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise Exception("No joystick detected!")

joystick = pygame.joystick.Joystick(0)
joystick.init()

try:
    print("Joystick control started. Press Ctrl+C to exit.")
    while True:
        pygame.event.pump()

        # Read joystick axes
        forward_backward = -joystick.get_axis(1)  # Invert for natural forward
        turn = joystick.get_axis(0)

        # Apply dead zone
        forward_backward = apply_dead_zone(forward_backward)
        turn = apply_dead_zone(turn)

        # Mix turning with forward/backward
        left_speed = forward_backward + turn
        right_speed = forward_backward - turn

        # Clamp values between -1.0 and 1.0
        left_speed = max(min(left_speed, 1.0), -1.0)
        right_speed = max(min(right_speed, 1.0), -1.0)

        set_motor_speed(left_motor, left_speed)
        set_motor_speed(right_motor, right_speed)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Stopping robot.")
    stop_motors()
    pygame.quit()

'''
pip install inputs
'''

import socket
import time
from inputs import get_gamepad

# JetBot IP and port
JETBOT_IP = '192.168.1.100'  # Replace with your JetBot's IP
PORT = 9999

# Connect to JetBot once
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((JETBOT_IP, PORT))
print("Connected to JetBot")

# Initialize state
axis_x = 0
axis_y = 0

def send_command(direction, speed):
    try:
        command = f"{direction},{speed}"
        sock.sendall(command.encode('utf-8'))
        print(f"Sent: {command}")
    except Exception as e:
        print(f"Error sending command: {e}")

def interpret_direction(x, y):
    threshold = 5000  # Adjust based on joystick sensitivity
    direction = "stop"
    speed = min(abs(x), abs(y)) / 32767.0  # Normalize speed

    if y < -threshold:
        direction = "forward"
    elif y > threshold:
        direction = "backward"
    elif x < -threshold:
        direction = "left"
    elif x > threshold:
        direction = "right"

    return direction, round(speed, 2)

try:
    while True:
        events = get_gamepad()
        for event in events:
            if event.code == "ABS_X":
                axis_x = event.state
            elif event.code == "ABS_Y":
                axis_y = event.state

        direction, speed = interpret_direction(axis_x, axis_y)
        send_command(direction, speed)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping control...")

finally:
    sock.close()

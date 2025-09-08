import socket
import pygame
import time

# JetBot IP and port
JETBOT_IP = '192.168.1.100'  # Replace with your JetBot's IP
PORT = 9999

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise Exception("No joystick connected")

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Function to send command to JetBot
def send_command(direction, speed):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((JETBOT_IP, PORT))
            command = f"{direction},{speed}"
            s.sendall(command.encode('utf-8'))
            print(f"Sent command: {command}")
    except Exception as e:
        print(f"Failed to send command: {e}")

print("Starting joystick control. Press Ctrl+C to exit.")

try:
    while True:
        pygame.event.pump()

        # Read axis values
        axis_y = joystick.get_axis(1)  # Forward/backward
        axis_x = joystick.get_axis(0)  # Left/right

        # Determine direction and speed
        speed = min(abs(axis_y), abs(axis_x))
        direction = "stop"

        if axis_y < -0.2:
            direction = "forward"
        elif axis_y > 0.2:
            direction = "backward"
        elif axis_x < -0.2:
            direction = "left"
        elif axis_x > 0.2:
            direction = "right"

        send_command(direction, round(speed, 2))
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Joystick control stopped.")
finally:
    pygame.quit()

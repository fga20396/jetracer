'''

pip install pygame
sudo apt install python3-tk
pip install ttkbootstrap

'''


import socket
import pygame
import time
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from threading import Thread

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

# Connect to JetBot once
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((JETBOT_IP, PORT))

# GUI setup
root = tb.Window(themename="flatly")  # or "darkly", "cosmo", etc
root.title("JetBot Joystick Controller")
root.geometry("300x200")

# Labels to show direction and speed
direction_label = tb.Label(root, text="Direction: stop", font=("Arial", 14))
direction_label.pack(pady=10)

speed_label = tb.Label(root, text="Speed: 0.0", font=("Arial", 14))
speed_label.pack(pady=10)

stop_button = tb.Button(root, text="STOP", command=stop_robot, bootstyle="danger")
stop_button.pack(pady=5)


# Stop button
def stop_robot():
    send_command("stop", 0.0)
    direction_label.config(text="Direction: stop")
    speed_label.config(text="Speed: 0.0")

stop_button = tb.Button(root, text="STOP", command=stop_robot, bg="red", fg="white", font=("Arial", 12))
stop_button.pack(pady=10)

# Function to send command to JetBot
def send_command(direction, speed):
    try:
        command = f"{direction},{speed}"
        sock.sendall(command.encode('utf-8'))
    except Exception as e:
        print(f"Error sending command: {e}")

# Joystick monitoring thread
def joystick_loop():
    while True:
        pygame.event.pump()

        axis_y = joystick.get_axis(1)
        axis_x = joystick.get_axis(0)

        speed = round(min(abs(axis_y), abs(axis_x)), 2)
        direction = "stop"

        if axis_y < -0.2:
            direction = "forward"
        elif axis_y > 0.2:
            direction = "backward"
        elif axis_x < -0.2:
            direction = "left"
        elif axis_x > 0.2:
            direction = "right"

        send_command(direction, speed)

        direction_label.config(text=f"Direction: {direction}")
        speed_label.config(text=f"Speed: {speed}")

        time.sleep(0.1)

# Start joystick thread
thread = Thread(target=joystick_loop, daemon=True)
thread.start()

# Start GUI loop
root.mainloop()

# Cleanup
sock.close()
pygame.quit()

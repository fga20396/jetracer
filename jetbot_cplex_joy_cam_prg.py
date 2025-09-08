'''

pip install pygame opencv-python pillow psutil
sudo apt install python3-tk

'''

import socket
import pygame
import time
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
import cv2
import psutil

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
root = tk.Tk()
root.title("JetBot Controller with Camera and Battery")
root.geometry("640x480")

# Labels
direction_label = tk.Label(root, text="Direction: stop", font=("Arial", 12))
direction_label.pack()

speed_label = tk.Label(root, text="Speed: 0.0", font=("Arial", 12))
speed_label.pack()

battery_label = tk.Label(root, text="Battery: Unknown", font=("Arial", 12))
battery_label.pack()

# Stop button
def stop_robot():
    send_command("stop", 0.0)
    direction_label.config(text="Direction: stop")
    speed_label.config(text="Speed: 0.0")

stop_button = tk.Button(root, text="STOP", command=stop_robot, bg="red", fg="white", font=("Arial", 12))
stop_button.pack(pady=5)

# Camera preview
camera_label = tk.Label(root)
camera_label.pack()

cap = cv2.VideoCapture(0)

def update_camera():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
    root.after(100, update_camera)

# Send command
def send_command(direction, speed):
    try:
        command = f"{direction},{speed}"
        sock.sendall(command.encode('utf-8'))
    except Exception as e:
        print(f"Error sending command: {e}")

# Joystick thread
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

# Battery thread
def battery_loop():
    while True:
        battery = psutil.sensors_battery()
        if battery:
            battery_label.config(text=f"Battery: {battery.percent}%")
        else:
            battery_label.config(text="Battery: Not available")
        time.sleep(5)

# Start threads
Thread(target=joystick_loop, daemon=True).start()
Thread(target=battery_loop, daemon=True).start()
update_camera()

# GUI loop
root.mainloop()

# Cleanup
sock.close()
cap.release()
pygame.quit()

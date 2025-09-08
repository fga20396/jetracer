import socket

# JetBot IP address and port
JETBOT_IP = '192.168.1.100'  # Replace with your JetBot's IP
PORT = 9999

def send_command(direction, speed):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((JETBOT_IP, PORT))
        command = f"{direction},{speed}"
        s.sendall(command.encode('utf-8'))
        print(f"Sent command: {command}")

# Example usage
send_command("forward", 0.5)
send_command("left", 0.3)
send_command("stop", 0.0)

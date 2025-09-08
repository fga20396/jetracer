import socket
from jetbot import Robot

# Initialize JetBot
robot = Robot()

# Set up server socket
HOST = ''  # Listen on all interfaces
PORT = 9999  # Port to listen on

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Listening for commands on port {PORT}...")

try:
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break

        # Expected format: "direction,speed"
        # Example: "forward,0.5"
        try:
            direction, speed = data.strip().split(',')
            speed = float(speed)

            if direction == "forward":
                robot.forward(speed)
            elif direction == "backward":
                robot.backward(speed)
            elif direction == "left":
                robot.left(speed)
            elif direction == "right":
                robot.right(speed)
            elif direction == "stop":
                robot.stop()
            else:
                print(f"Unknown direction: {direction}")
        except Exception as e:
            print(f"Error processing command: {e}")

except KeyboardInterrupt:
    print("Shutting down.")

finally:
    robot.stop()
    server_socket.close()

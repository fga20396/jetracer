from jetbot import Camera
import cv2
import numpy as np
import time
import os

# Create a directory to store captured images
save_dir = "captured_images"
os.makedirs(save_dir, exist_ok=True)

# Initialize the camera
camera = Camera.instance()

try:
    print("Starting periodic image capture. Press Ctrl+C to stop.")
    while True:
        # Capture image
        image = camera.value

        # Convert RGB to BGR for OpenCV
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Create filename with timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(save_dir, f"image_{timestamp}.jpg")

        # Save image
        cv2.imwrite(filename, image_bgr)
        print(f"Saved {filename}")

        # Wait for 10 seconds
        time.sleep(10)

except KeyboardInterrupt:
    print("Image capture stopped by user.")

finally:
    camera.stop()

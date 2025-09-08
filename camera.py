import cv2

class Camera:
    def __init__(self, width=224, height=224, capture_device=0, format='jpeg'):
        self._width = width
        self._height = height
        self._capture_device = capture_device
        self._format = format

        self.cap = cv2.VideoCapture(self._capture_device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, value)

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read from camera")
        return frame

    def release(self):
        self.cap.release()

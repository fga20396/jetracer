class Robot:
    def __init__(self, left_motor, right_motor, speed=0.3):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self._speed = speed
        self._update_motor_speed()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    speed(self, value):
        self._speed = value
        self._update_motor_speed()

    def _update_motor_speed(self):
        self.left_motor.alpha = self._speed
        self.right_motor.alpha = self._speed

    def forward(self, value=1.0):
        self.left_motor.value = value
        self.right_motor.value = value

    def backward(self, value=1.0):
        self.left_motor.value = -value
        self.right_motor.value = -value

    def left(self, value=1.0):
        self.left_motor.value = -value
        self.right_motor.value = value

    def right(self, value=1.0):
        self.left_motor.value = value
        self.right_motor.value = -value

    def stop(self):
        self.left_motor.value = 0.0
        self.right_motor.value = 0.0

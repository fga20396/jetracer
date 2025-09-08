class Motor:
    def __init__(self, driver, channel, alpha=1.0, beta=0.0):
        self._driver = driver
        self._channel = channel
        self._value = 0.0
        self.alpha = alpha
        self.beta = beta

        self._motor = self._driver.getMotor(channel)
        self._ina, self._inb = (1, 0) if channel == 1 else (2, 3)

        import atexit
        atexit.register(self._release)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._write_value(new_value)

    def _write_value(self, value):
        mapped_value = int(255.0 * (self.alpha * value + self.beta))
        speed = min(max(abs(mapped_value), 0), 255)
        self._motor.setSpeed(speed)

        if mapped_value < 0:
            self._motor.run(Adafruit_MotorHAT.FORWARD)
            self._driver._pwm.setPWM(self._ina, 0, 0)
            self._driver._pwm.setPWM(self._inb, 0, speed * 16)
        else:
            self._motor.run(Adafruit_MotorHAT.BACKWARD)
            self._driver._pwm.setPWM(self._ina, 0, speed * 16)
            self._driver._pwm.setPWM(self._inb, 0, 0)

    def _release(self):
        self._motor.run(Adafruit_MotorHAT.RELEASE)
        self._driver._pwm.setPWM(self._ina, 0, 0)
        self._driver._pwm.setPWM(self._inb, 0, 0)

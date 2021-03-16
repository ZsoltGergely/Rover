import wiringpi

# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 73  # 19.2 MHz / 2 / 480 = 20 kHz
MAX_SPEED = _max_speed

rpi_pwm = []  # 12, 13, 18, 19]

"""
def io_init():
    global io_initialized
    if io_initialized:
        return

    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(12, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pinMode(13, wiringpi.GPIO.PWM_OUTPUT)

    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
    wiringpi.pwmSetRange(MAX_SPEED)
    wiringpi.pwmSetClock(2)

    wiringpi.pinMode(5, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(6, wiringpi.GPIO.OUTPUT)

    io_initialized = True
"""

wiringpi.wiringPiSetupGpio()


class Motor:
    def __init__(self, IN1, IN2):
        self.IN1 = IN1
        self.IN2 = IN2

        wiringpi.pinMode(IN1, wiringpi.GPIO.OUTPUT)
        wiringpi.pinMode(IN2, wiringpi.GPIO.OUTPUT)

        wiringpi.softPwmCreate(IN1, 0, MAX_SPEED)
        wiringpi.softPwmCreate(IN2, 0, MAX_SPEED)

    def reverse(self, speed=MAX_SPEED):
        wiringpi.softPwmWrite(self.IN1, wiringpi.GPIO.LOW)
        wiringpi.softPwmWrite(self.IN2, min(MAX_SPEED, abs(speed)))

    def forward(self, speed=MAX_SPEED):
        wiringpi.softPwmWrite(self.IN2, wiringpi.GPIO.LOW)
        wiringpi.softPwmWrite(self.IN1, min(MAX_SPEED, abs(speed)))

    def setSpeed(self, speed):
        if speed < 0:
            self.reverse(-speed)
        else:
            self.forward(speed)

    def stop(self):
        self.setSpeed(0)

    def brake(self):
        wiringpi.softPwmWrite(self.IN2, MAX_SPEED)
        wiringpi.softPwmWrite(self.IN1, MAX_SPEED)



class DRV8833:
    def __init__(self, A1, A2, B1, B2):
        self.motorA=Motor(A1, A2)
        self.motorB=Motor(B1, B2)


    def stop(self, A = True, B = True):

        if A:
            self.motorA.stop()
        if B:
            self.motorB.stop()

    def setSpeeds(self, speedA=None, speedB=None):
        if speedA is not None:
            self.motorA.setSpeed(speedA)
        if speedB is not None:
            self.motorB.setSpeed(speedB)

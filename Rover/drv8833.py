import RPi.GPIO as GPIO

# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 10  # 19.2 MHz / 2 / 480 = 20 kHz
MAX_SPEED = _max_speed

PWM_FREQ = 100

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


class Motor:
    def __init__(self, IN1, IN2, maxRPM):
        self.IN1 = IN1
        self.IN2 = IN2

        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)

        self.pwm1 = GPIO.PWM(IN1, 100)
        self.pwm2 = GPIO.PWM(IN2, 100)
        self.pwm1.start(0)
        self.pwm2.start(0)

        self.MAX_SPEED = maxRPM

    def __reverse(self, speed):
        duty = min(self.MAX_SPEED, speed) * 100 / self.MAX_SPEED
        # print(duty)
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(duty)

    def __forward(self, speed):
        duty = min(self.MAX_SPEED, speed) * 100 / self.MAX_SPEED
        # print(duty)
        self.pwm1.ChangeDutyCycle(duty)
        self.pwm2.ChangeDutyCycle(0)

    def setSpeed(self, speed):
        if speed < 0:
            self.__reverse(-speed)
        else:
            self.__forward(speed)

    def stop(self):
        self.setSpeed(0)


class DRV8833:
    def __init__(self, A1, A2, B1, B2, maxA=MAX_SPEED, maxB=MAX_SPEED):
        self.motorA = Motor(A1, A2, maxA)
        self.motorB = Motor(B1, B2, maxB)

    def stop(self, A=True, B=True):

        if A:
            self.motorA.stop()
        if B:
            self.motorB.stop()

    def setSpeeds(self, speedA=None, speedB=None):
        if speedA is not None:
            self.motorA.setSpeed(speedA)
        if speedB is not None:
            self.motorB.setSpeed(speedB)


def init():
    GPIO.setmode(GPIO.BCM)


def close():
    GPIO.cleanup()



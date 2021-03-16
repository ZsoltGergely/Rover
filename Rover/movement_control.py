import drv8833
from maestro import *
import config
import math
from time import time, sleep
import threading

"""==============INIT=============="""

# Motor and steering control

fw_motors = drv8833.DRV8833(config.E_BAL_M[0], config.E_BAL_M[1], config.E_JOBB_M[0], config.E_JOBB_M[1])
bw_motors = drv8833.DRV8833(config.H_BAL_M[0], config.H_BAL_M[1], config.H_JOBB_M[0], config.H_JOBB_M[1])

balElso = Servo(0, -90, 90, config.PWM_MG90S["min"], config.PWM_MG90S["max"], 0, accel=10)
jobbElso = Servo(1, -90, 90, config.PWM_MG90S["min"], config.PWM_MG90S["max"], 0, accel=10)
balHatso = Servo(2, -90, 90, config.PWM_MG90S["min"], config.PWM_MG90S["max"], 0, accel=10)
jobbHatso = Servo(3, -90, 90, config.PWM_MG90S["min"], config.PWM_MG90S["max"], 0, accel=10)

speeds = [0, 0, 0, 0]
targets = [0, 0, 0, 0]
end_time = time()
timeBased = False
distanceBased = False

CIR_ANGLE = 50

# Arm control

servo_1 = Servo(7, min_pulse=config.PWM_MM0090["min"], max_pulse=config.PWM_MM0090["max"], default=0)
servo_2 = Servo(8, min_pulse=config.PWM_MM0090["min"], max_pulse=config.PWM_MM0090["max"], default=-90)
servo_3 = Servo(9, min_pulse=config.PWM_MM0090["min"], max_pulse=config.PWM_MM0090["max"], default=-30)
servo_4 = Servo(10, min_pulse=config.PWM_MG90S["min"], max_pulse=config.PWM_MG90S["max"], default=90)
servo_gripper = Servo(11, min_pulse=config.PWM_MG90S["min"], max_pulse=config.PWM_MG90S["max"], default=60)

# Camera control

camServo = Servo(5, -90, 90, config.PWM_SG90["min"], config.PWM_SG90["max"])


def setAszt(servo_elol_bal=None, servo_elol_jobb=None, servo_hatul_bal=None, servo_hatul_jobb=None,
            motor_elol_bal=None, motor_elol_jobb=None, motor_hatul_bal=None, motor_hatul_jobb=None):
    # motorok meg kormányzó szervók

    if servo_elol_bal is not None:
        balElso.write(servo_elol_bal)
    if servo_elol_jobb is not None:
        jobbElso.write(servo_elol_jobb)
    if servo_hatul_bal is not None:
        balHatso.write(servo_hatul_bal)
    if servo_hatul_jobb is not None:
        jobbHatso.write(servo_hatul_jobb)

    speeds[0] = motor_elol_bal
    speeds[1] = motor_elol_jobb
    speeds[2] = motor_hatul_bal
    speeds[3] = motor_hatul_jobb


def thread4motorControl():
    while True:
        _speeds = [0, 0, 0, 0]
        if timeBased and end_time >= time():
            fw_motors.setSpeeds(speedA=_speeds[0], speedB=_speeds[1])
            bw_motors.setSpeeds(speedA=_speeds[2], speedB=_speeds[3])
        sleep(0.1)


def moveAtAngleFW(speed, angle=None):
    setAszt(angle, angle, 0, 0, speed, speed, speed, speed)


def moveAtAngleBW(speed, angle=None):
    setAszt(0, 0, angle, angle, speed, speed, speed, speed)


def moveAtAngle(speed, angle=None):
    setAszt(angle, angle, 0, 0, speed, speed, speed, speed)
    # setAszt(0, 0, angle, angle, speed, speed, speed, speed)


def moveAroundCirc(speed, angle=None):
    setAszt(angle, angle, -angle, -angle, speed, speed, speed, speed)


def turn(speed, direction: bool):
    angle = CIR_ANGLE
    speed = speed if direction else -speed
    setAszt(angle, -angle, -angle, angle, speed, -speed, speed, -speed)


def stop():
    setAszt(None, None, None, None, 0, 0, 0, 0)


"""=======ARM CONTROL======"""


def setArm(s1, s2, s3, s4, g):
    if s1 is not None:
        servo_1.write(s1)
    if s2 is not None:
        servo_2.write(s2)
    if s3 is not None:
        servo_3.write(s3)
    if s4 is not None:
        servo_4.write(s4)

    if g is not None and -50 <= g < 80:
        servo_gripper.write(g)


class Pont:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None


def fokba(a):
    b = a * 180 / math.pi
    return b


class Kar:
    def __init__(self):
        self.a1 = None
        self.a2 = None
        self.a3 = None
        self.a4 = None
        self.l1 = 2
        self.l2 = 2
        self.l3 = 2
        self.A = Pont()
        self.B = Pont()

    def set_szogek(self, szog, P):
        if P.x == 0:
            self.a1 = math.pi / 2
        else:
            self.a1 = math.atan(P.y / P.x)
        self.B.z = P.z + math.sin(szog) * self.l3
        self.B.x = P.x - math.cos(self.a1) * (math.cos(szog) * self.l3)
        self.B.y = P.y - math.sin(self.a1) * (math.cos(szog) * self.l3)

        try:
            self.a3 = math.pi - math.acos(
                (self.l1 * 2 + self.l2 * 2 - self.B.x * 2 - self.B.y * 2 - self.B.z ** 2) / (2 * self.l1 * self.l2))
        except:
            print('Tul messze van')
            return

        self.a2 = math.asin(self.B.z / (math.sqrt(self.B.x * 2 + self.B.y * 2 + self.B.z ** 2))) + math.asin(
            math.sin(self.a3) * self.l2 / (math.sqrt(self.B.x * 2 + self.B.y * 2 + self.B.z ** 2)))

        self.A.z = math.sin(self.a2) * self.l1
        self.A.x = math.cos(self.a1) * math.cos(self.a2) * self.l1
        self.A.y = math.sin(self.a1) * math.cos(self.a2) * self.l1

        d = math.sqrt((P.x - self.A.x) * 2 + (P.y - self.A.y) * 2 + (P.z - self.A.z) ** 2)

        self.a4 = math.pi - math.acos((self.l3 * 2 + self.l2 * 2 - d ** 2) / (2 * self.l1 * self.l2))

        self.a3 = -self.a3

        Tmp = Pont()
        Tmp.x = (self.A.x + P.x) / 2
        Tmp.y = (self.A.y + P.y) / 2
        Tmp.z = (self.A.z + P.z) / 2
        if (Tmp.z < self.B.z):
            self.a4 = -self.a4
        return self.a1, self.a2, self.a3, self.a4


""""========CAMERA CONTROL POSITION======"""


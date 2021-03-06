import drv8833
from maestro import *
import config
import math
from time import time

"""==============POSITIONING CONTROL=============="""

"""==============INIT=============="""

fw_motors = drv8833.DRV8833(config.E_BAL_M[0], config.E_BAL_M[1], config.E_JOBB_M[0], config.E_JOBB_M[1])
bw_motors = drv8833.DRV8833(config.H_BAL_M[0], config.H_BAL_M[1], config.H_JOBB_M[0], config.H_JOBB_M[1])

balElso = Servo(0, config.PWM_MG90S, [-90, 90])
jobbElso = Servo(1, config.PWM_MG90S, [-90, 90])
balHatso = Servo(2, config.PWM_MG90S, [-90, 90])
jobbHatso = Servo(3, config.PWM_MG90S, [-90, 90])


def moveAtAngleFW(speed, angle=None):
    if angle is not None:
        balElso.write(angle)
        jobbElso.write(angle)
        balHatso.write(0)
        jobbHatso.write(0)
    fw_motors.setSpeeds(speed, speed)
    bw_motors.setSpeeds(speed, speed)


def moveAtAngleBW(speed, angle=None):
    if angle is not None:
        balElso.write(0)
        jobbElso.write(0)
        balHatso.write(angle)
        jobbHatso.write(angle)
    fw_motors.setSpeeds(speed, speed)
    bw_motors.setSpeeds(speed, speed)


def moveAtAngle(speed, angle=None):
    if angle is not None:
        balElso.write(angle)
        jobbElso.write(angle)
        balHatso.write(0)
        jobbHatso.write(0)
    fw_motors.setSpeeds(speed, speed)
    bw_motors.setSpeeds(speed, speed)


def moveAroundCirc(speed, angle=None):
    if angle is not None:
        balElso.write(angle)
        jobbElso.write(angle)
        balHatso.write(-angle)
        jobbHatso.write(-angle)
    fw_motors.setSpeeds(speed, speed)
    bw_motors.setSpeeds(speed, speed)


CIR_ANGLE = 50


def turn(speed, direction: bool):
    angle = CIR_ANGLE

    balElso.write(angle)
    jobbElso.write(angle)
    balHatso.write(-angle)
    jobbHatso.write(-angle)

    speed = speed if direction else -speed

    fw_motors.setSpeeds(speed, -speed)
    bw_motors.setSpeeds(-speed, speed)

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
        if (P.x == 0):
            self.a1 = math.pi / 2
        else:
            self.a1 = math.atan(P.y / P.x)
        self.B.z = P.z + math.sin(szog) * self.l3
        self.B.x = P.x - math.cos(self.a1) * (math.cos(szog) * self.l3)
        self.B.y = P.y - math.sin(self.a1) * (math.cos(szog) * self.l3)

        try:
            self.a3 = math.pi - math.acos((self.l1 * 2 + self.l2 * 2 - self.B.x * 2 - self.B.y * 2 - self.B.z ** 2) / (2 * self.l1 * self.l2))
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
        Tmp.x = (self.A.x + P.x)/2
        Tmp.y = (self.A.y + P.y)/2
        Tmp.z = (self.A.z + P.z)/2
        if(Tmp.z < self.B.z):
            self.a4 = -self.a4
        return self.a1, self.a2, self.a3, self.a4

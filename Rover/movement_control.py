import drv8833
import maestro
import config
import math
from time import time, sleep
import kar as kar
import threading

"""==============INIT=============="""

# global fw_motors, bw_motors, balElso, balHatso, jobbElso, jobbHatso, \
#     servo_1, servo_2, servo_3, servo_4, servo_gripper, camServo

speeds = [0, 0, 0, 0]
_speeds = [0, 0, 0, 0]
targets = [0, 0, 0, 0]
end_time = time()
timeBased = False
distanceBased = False
arm=kar.Kar()
pont=kar.Pont()

WIDTH = 25
LENGTH = 30

CIR_ANGLE = math.degrees(math.atan(LENGTH/WIDTH))

servoNumbering = [7, 8, 9,10]

def init():
    drv8833.init()
    maestro.init()

    global fw_motors, bw_motors, balElso, balHatso, jobbElso, jobbHatso, \
        servo_1, servo_2, servo_3, servo_4, servo_gripper, camServo, end_time

    # Motor and steering control

    fw_motors = drv8833.DRV8833(config.E_BAL_M[0], config.E_BAL_M[1], config.E_JOBB_M[0], config.E_JOBB_M[1], 110, 110)
    bw_motors = drv8833.DRV8833(config.H_BAL_M[0], config.H_BAL_M[1], config.H_JOBB_M[0], config.H_JOBB_M[1], 33, 33)

    balElso = maestro.Servo(servoNumbering[0], -90, 90, config.PWM_MG90S["min"], config.PWM_MG90S["max"], 0, accel=10)
    jobbElso = maestro.Servo(servoNumbering[1], -90, 90, config.PWM_MG90S["min"], config.PWM_MG90S["max"], 0, accel=10)
    balHatso = maestro.Servo(servoNumbering[2], -90, 90, config.PWM_MG90S["min"], config.PWM_MG90S["max"], 0, accel=10)
    jobbHatso = maestro.Servo(servoNumbering[3], -90, 90, config.PWM_MG90S["min"], config.PWM_MG90S["max"], 0, accel=10)

    # Arm control

    servo_1 = maestro.Servo(0, min_pulse=config.PWM_MM0090["min"], max_pulse=config.PWM_MM0090["max"], default=0,
                            accel=60)
    servo_2 = maestro.Servo(1, min_pulse=config.PWM_MM0090["min"], max_pulse=config.PWM_MM0090["max"], default=-90,
                            accel=60)
    servo_3 = maestro.Servo(2, min_pulse=config.PWM_MM0090["min"], max_pulse=config.PWM_MM0090["max"], default=-30,
                            accel=60)
    servo_4 = maestro.Servo(3, min_pulse=config.PWM_MG90S["min"], max_pulse=config.PWM_MG90S["max"], default=90,
                            accel=60)
    servo_gripper = maestro.Servo(4, min_pulse=config.PWM_MG90S["min"], max_pulse=config.PWM_MG90S["max"], default=60,
                                  accel=60)

    # Camera control

    camServo = maestro.Servo(5, -90, 90, config.PWM_SG90["min"], config.PWM_SG90["max"])

    global controlThread, timeBased

    controlThread = threading.Thread(target=thread4motorControl, daemon=True)
    controlThread.start()

    timeBased=True


def setAszt(servo_elol_bal=None, servo_elol_jobb=None, servo_hatul_bal=None, servo_hatul_jobb=None,
            motor_elol_bal=None, motor_elol_jobb=None, motor_hatul_bal=None, motor_hatul_jobb=None, timer=5):
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
    global end_time
    end_time = time() + timer


def close():
    stop()
    drv8833.close()
    maestro.close()


def thread4motorControl():
    global _speeds
    while True:
        if maestro.servos.isMoving(servoNumbering[0]) or maestro.servos.isMoving(servoNumbering[1]) or\
                maestro.servos.isMoving(servoNumbering[2]) or maestro.servos.isMoving(servoNumbering[3]):
            continue
        _speeds = speeds
        if timeBased and end_time >= time():
            fw_motors.setSpeeds(speedA=_speeds[0], speedB=_speeds[1])
            bw_motors.setSpeeds(speedA=_speeds[2], speedB=_speeds[3])
            # print("aaa")
        elif timeBased and end_time < time():
            fw_motors.setSpeeds(speedA=0, speedB=0)
            bw_motors.setSpeeds(speedA=0, speedB=0)
        sleep(0.1)


#
# /-----/
#    |
#    |
# |-----|
#

def moveAtAngleFW(speed, angle=None, timer=None):
    # angleB = math.degrees(math.atan(1/(1/math.tan(angle)-WIDTH/LENGTH)))*math.copysign(1, angle)
    # angleA = math.degrees(math.atan(1/(1/math.tan(angle)-WIDTH/LENGTH)))
    setAszt(angle, angle, 0, 0, speed, speed, speed, speed, timer if timer is not None else 60)


# def moveAtAngleBW(speed, angle=None, timer=None):
#     setAszt(0, 0, angle, angle, speed, speed, speed, speed, timer if timer is not None else 60)


def moveAtAngle(speed, angle=None, timer=None):
    setAszt(angle, angle, 0, 0, speed, speed, speed, speed, timer if timer is not None else 60)
    # setAszt(0, 0, angle, angle, speed, speed, speed, speed)

#
# /-----/
#    |
#    |
# \-----\
#

def moveAroundCirc(speed, angle=None, timer=None):

    setAszt(angle, angle, -angle, -angle, speed, speed, speed, speed, timer if timer is not None else 60)


#
# /-----\
#    |
#    |
# \-----/
#


def turn(speed, direction: bool, timer=None):
    angle = CIR_ANGLE
    speed = speed if direction else -speed
    setAszt(angle, -angle, -angle, angle, speed, -speed, speed, -speed, timer if timer is not None else 60)


def stop():
    setAszt(None, None, None, None, 0, 0, 0, 0)


"""=======ARM CONTROL======"""

# Home pos 0 -90 -30 90 60
def setArm(s1=0, s2=-90, s3=-30, s4=90, g=60):
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


def moveArmToPos(x, y, z, gamma=90):
    global pont
    pont = kar.Pont(x, y, z)
    szogek = arm.set_szogek(gamma, pont)
    print(szogek)
    if szogek is not None:
        setArm(szogek[0], szogek[1], szogek[2], szogek[3])
    else:
        setArm()

""""========CAMERA CONTROL POSITION======"""

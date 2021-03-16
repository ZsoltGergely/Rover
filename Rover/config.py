"""==========   PINOUT  =========="""

# DC motrok pin
# motor_name_M = [IN1, IN2]

E_JOBB_M = [26, 19]
E_BAL_M = [13, 11]

H_JOBB_M = [21, 20]
H_BAL_M = [16, 12]

# direction servo
# servo_name_S = [order_on_maestro, Left_max, Right_max]

PWM_MG90S = {
    "min":400*4,
    "max":2432*4,
    "total":180
}
PWM_MM0090 = {
    "min":480*4,
    "max":2368*4,
    "total":180
}
PWM_SG90 = {
    "min":554*4,
    "max":2352*4,
    "total":180
}

E_JOBB_S = [0, PWM_MG90S]
E_BAL_S = [1]

H_JOBB_S = [2]
H_BAL_S = [3]

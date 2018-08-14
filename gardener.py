from Raspi_PWM_Servo_Driver import PWM
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

import time
import atexit

mh = Raspi_MotorHAT(addr=0x6f)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

pwm = PWM(0x6F)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

offset = 45

pwm.setPWMFreq(60)

myMotor = mh.getMotor(2)

# 12V instead of 14V!
myMotor.setSpeed(220)

def hose(n):
        angles  = [85,85,81,76,75,75]
        new_position = (servoMax - offset) - (n * angles[n])
        pwm.setPWM(0, 0, new_position)
        time.sleep(1.0)

def pumpWater(n):
        myMotor.run(Raspi_MotorHAT.BACKWARD);
        time.sleep(n)
        myMotor.run(Raspi_MotorHAT.RELEASE);
        time.sleep(0.5)


def move_from_to(start, end):
        for i in range(start, end):
                hose(i)
        for i in range(end, start, -1):
                hose(i)



# while(True):
#   move_from_to(0,5)

# count = 0
# while(True):
#         count = count + 1
#         print(count, " iteration")
#         hose(1)
#         pumpWater(3)
#         hose(2)
#         pumpWater(2)
#         for i in range(0, 5):
#                 print(i, " minutes")
#                 time.sleep(60)

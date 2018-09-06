from Raspi_PWM_Servo_Driver import PWM
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from filelock import Timeout, FileLock

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
        angles  = [0,80,150, 85 * 3, 87 * 4, 88 * 5]
        new_position = (servoMax - offset) - (angles[n])
        pwm.setPWM(0, 0, new_position)
        time.sleep(1.0)

def pump_water(n):
        myMotor.run(Raspi_MotorHAT.BACKWARD);
        time.sleep(n)
        myMotor.run(Raspi_MotorHAT.RELEASE);
        time.sleep(0.5)

def move_from_to(start, end):
        for i in range(start, end):
                hose(i)
        for i in range(end, start, -1):
                hose(i)

def test_positions():
    lock_path = "/home/pi/gardener/locks/gardener.txt.lock"
    gardener_lock = FileLock(lock_path, timeout=100)
    try:
        gardener_lock.acquire(timeout=0.1)
        move_from_to(2,5)
        return True
    except Timeout:
        return False
    finally:
        gardener_lock.release()


def irrigate(n, amount):
    lock_path = "/home/pi/gardener/locks/gardener.txt.lock"
    gardener_lock = FileLock(lock_path, timeout=100)
    try:
        gardener_lock.acquire(timeout=0.1)
        hose(n)
        # time.sleep(amount)
        pump_water(amount)
        return True
    except Timeout:
        return False
    finally:
        gardener_lock.release()

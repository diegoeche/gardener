import os
import serial, time
from app import *

SENSOR_PATH=os.environ['SENSOR']
ser = serial.Serial(SENSOR_PATH, 9600)

sensor_buffer = []

while 1:
    serial_line = ser.readline()
    value = float(serial_line)
    if (value <= 1024):
        sd = SensorData(sensor_id=1, value=float(serial_line))
        db.session.add(sd)
        db.session.commit()
    time.sleep(0.1)


ser.close() # Only executes once the loop exits

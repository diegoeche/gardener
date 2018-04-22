import serial, time
from app import *

ser = serial.Serial('/dev/tty.wchusbserial1420', 9600)

sensor_buffer = []

while 1:
    serial_line = ser.readline()
    print(serial_line)
    sd = SensorData(sensor_id=1, value=float(serial_line))
    db.session.add(sd)
    db.session.commit()
    time.sleep(0.1)


ser.close() # Only executes once the loop exits

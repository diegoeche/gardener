import os
import serial, time
from app import *

SENSOR_PATH=os.environ['SENSOR']
ser = serial.Serial(SENSOR_PATH, 9600)

sensor_buffer = []

while 1:
    serial_line = ser.readline()
    values = serial_line.split(",")
    print(values)
    if values[0] == "START" and (len(values) == 5):
        sensor_id = 1
        for value in values[1:]:
            parsed_value = float(value)
            if (parsed_value <= 1024):
                sd = SensorData(sensor_id=sensor_id, value=parsed_value)
                db.session.add(sd)
            sensor_id = sensor_id + 1

        db.session.commit()
        time.sleep(0.1)

ser.close() # Only executes once the loop exits

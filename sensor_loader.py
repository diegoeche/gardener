import os
import serial, time
from app import *
from influxdb import InfluxDBClient

SENSOR_PATH=os.environ['SENSOR']
ser = serial.Serial(SENSOR_PATH, 9600)

sensor_buffer = []

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'gardener_db')

def add_to_influxdb(sensor_id, value):
    json_body = [
        {
            "measurement": "SENSOR_%s" % sensor_id,
            "fields": {
                "value": value
            }
        }
    ]
    client.write_points(json_body)


while 1:
    serial_line = ser.readline()
    values = serial_line.split(",")
    print(values)
    if values[0] == "START" and (len(values) == 5):
        sensor_id = 1
        for value in values[1:]:
            parsed_value = float(value)
            if (parsed_value <= 1024):
                add_to_influxdb(sensor_id, parsed_value)
            sensor_id = sensor_id + 1
        time.sleep(0.1)

ser.close() # Only executes once the loop exits

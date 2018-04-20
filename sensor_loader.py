import serial, time

ser = serial.Serial('/dev/tty.wchusbserial1410', 9600)

while 1:
    serial_line = ser.readline()
    print(serial_line) # If using Python 2.x use: print serial_line
    # Do some other work on the data
    time.sleep(0.5) # sleep 5 minutes
    # Loop restarts once the sleep is finished

ser.close() # Only executes once the loop exits

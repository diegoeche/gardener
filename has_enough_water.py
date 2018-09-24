#!/bin/python

from app import *

import sys

ARGUMENTS = sys.argv
if len(ARGUMENTS) > 2:
    sensor = int(sys.argv[1])
    test_value = float(sys.argv[2])
    value = current_value(int(sensor), 1024)
    print("Current Humidity: ", value)

    if(value < test_value):
        print("Not enough water")
        exit(0)
    else:
        print("Enough water")
        exit(1)

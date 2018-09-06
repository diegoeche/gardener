# A simple wrapper for command-line irrigation
from gardener import irrigate
import sys

ARGUMENTS = sys.argv
if len(ARGUMENTS) > 2:
    sensor = int(sys.argv[1])
    amount = int(sys.argv[2])
    irrigate(sensor, amount)

# A simple wrapper for command-line irrigation
from gardener import irrigate
import sys

ARGUMENTS = sys.argv
if len(ARGUMENTS) > 1:
    irrigate(int(sys.argv[1]))

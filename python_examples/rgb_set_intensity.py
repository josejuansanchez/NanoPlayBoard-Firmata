#!/usr/bin/python
import time
import sys

from nanoplayboard import NanoPlayBoard

if len(sys.argv) != 2:
    print('Usage: python {0} <serial_port_used>'.format(sys.argv[0]))
    print('You have to specify the serial port used by the NanoPlayBoard.')
    sys.exit(-1)

port = sys.argv[1]

board = NanoPlayBoard(port)
board.rgb_on()

for intensity in range(0, 101, 25):
    board.rgb_set_intensity(intensity)
    print(intensity)
    time.sleep(0.2)

for intensity in range(100, 0, -25):
    board.rgb_set_intensity(intensity)
    print(intensity)
    time.sleep(0.2)

board.rgb_off()
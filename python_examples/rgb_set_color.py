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

while 1:
    board.rgb_set_color(255, 0, 0)
    time.sleep(1)
    board.rgb_set_color(0, 255, 0)
    time.sleep(1)
    board.rgb_set_color(0, 0, 255)
    time.sleep(1)
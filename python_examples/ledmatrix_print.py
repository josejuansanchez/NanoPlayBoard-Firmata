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
pattern = [16, 72, 8, 72, 16]

while 1:
    board.ledmatrix_print(pattern)
    time.sleep(0.019)

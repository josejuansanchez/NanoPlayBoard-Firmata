#!/usr/bin/python
import time
import sys

from nanoplayboard import NanoPlayBoard

if len(sys.argv) != 2:
    print('Usage: python {0} <serial_port_used>'.format(sys.argv[0]))
    print('You have to specify the serial port used by the NanoPlayBoard.')
    sys.exit(-1)

port = sys.argv[1]

def new_data_received(value):
    print('Potentiometer: {0}'.format(value))
    board.ledmatrix_print_in_landscape(value)

board = NanoPlayBoard(port)

while 1:
    board.potentiometer_scale_to(0, 99, new_data_received)
    time.sleep(0.020)

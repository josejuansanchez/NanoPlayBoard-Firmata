#!/usr/bin/python
import time
import sys

from nanoplayboard import NanoPlayBoard

if len(sys.argv) != 2:
    print('Usage: python {0} <serial_port_used>'.format(sys.argv[0]))
    print('You have to specify the serial port used by the NanoPlayBoard.')
    sys.exit(-1)

port = sys.argv[1]

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def new_data_received(value):
    intensity = map(value, 0, 1023, 0, 100)
    board.rgb_set_intensity(intensity)
    print('Potentiometer: {0} - Intensity: {1}'.format(value, intensity))    

board = NanoPlayBoard(port)

while 1:
    board.potentiometer_read(new_data_received)
    time.sleep(0.02)

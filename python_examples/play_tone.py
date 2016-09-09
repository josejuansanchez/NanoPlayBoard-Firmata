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
board.play_tone(440)
time.sleep(0.25)
board.stop_tone()
time.sleep(1)

board.play_tone(440, 1000)
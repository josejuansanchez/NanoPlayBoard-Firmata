"""
 NanoPlayBoard PyMata helper class.

 This is not an example, rather it's a class to add NanoPlayBoard-specific
 commands to PyMata.  Make sure this file is in the same directory as the
 examples!

 This class is based on the circuitplayground.py developed by: Tony DiCola

  Copyright (C) 2016 Tony DiCola.  All rights reserved.
  Copyright (C) 2016 Jose Juan Sanchez.  All rights reserved.

 Licensed under the GNU General Public License, Version 3 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

    http://www.gnu.org/licenses/gpl-3.0.en.html

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import logging
import struct
from binascii import hexlify
from PyMata.pymata import PyMata

NPB_COMMAND                 = 0x40  # Byte that identifies all NanoPlayBoard commands.
NPG_BUZZER_PLAY_TONE        = 0x20  # Play a tone on the speaker. Sends next values:
                                    #  - Frequency (hz). 2 7-bit bytes
                                    #    (up to 2^14 hz, about 16khz)
                                    #  - Duration (ms). 2 7-bit bytes
                                    #    (up to 2^14 ms, about 16s)
NPG_BUZZER_STOP_TONE        = 0x21  # Stop playing anything on the speaker.

NPB_RGB_ON                  = 0x30
NPB_RGB_OFF                 = 0x31
NPB_RGB_TOGGLE              = 0x32
NPB_RGB_SET_COLOR           = 0x33
NPB_RGB_SET_INTENSITY       = 0x34

NPB_POTENTIOMETER_READ      = 0x40
NPB_POTENTIOMETER_SCALE_TO  = 0x41

NPB_LDR_READ                = 0x50
NPB_LDR_SCALE_TO            = 0x51

NPB_LEDMATRIX_PRINT_CHAR    = 0x60
NPB_LEDMATRIX_PRINT_PATTERN = 0x61
NPB_LEDMATRIX_PRINT_STRING  = 0x62
NPB_LEDMATRIX_PRINT_IN_LAND = 0x63


logger = logging.getLogger(__name__)

class NanoPlayBoard(PyMata):
    def __init__(self, port_id='/dev/ttyACM0', bluetooth=True, verbose=True):
        PyMata.__init__(self, port_id, bluetooth, verbose)
        self._command_handler.command_dispatch.update({NPB_COMMAND: [self._response_handler, 1]})
        self._potentiometer_callback = None
        self._ldr_callback = None

    def play_tone(self, frequency_hz, duration_ms=0):
        # Note:
        # 0x3FFF = 0011 1111 1111 1111
        # 0x7F   =           0111 1111

        # Pack 14-bits into 2 7-bit bytes.
        frequency_hz &= 0x3FFF
        f1 = frequency_hz & 0x7F
        f2 = frequency_hz >> 7
        
        # Pack 14-bits into 2 7-bit bytes.
        duration_ms &= 0x3FFF
        d1 = duration_ms & 0x7F
        d2 = duration_ms >> 7
        self._command_handler.send_sysex(NPB_COMMAND, [NPG_BUZZER_PLAY_TONE, f1, f2, d1, d2])

    def stop_tone(self):
        self._command_handler.send_sysex(NPB_COMMAND, [NPG_BUZZER_STOP_TONE])

    def rgb_on(self):
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_RGB_ON])

    def rgb_off(self):
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_RGB_OFF])

    def rgb_toggle(self):
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_RGB_TOGGLE])

    def rgb_set_color(self, red, green, blue):
        red &= 0xFF
        green &= 0xFF
        blue &= 0xFF
        b1 = red >> 1
        b2 = ((red & 0x01) << 6) | (green >> 2)
        b3 = ((green & 0x03) << 5) | (blue >> 3)
        b4 = (blue & 0x07) << 4
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_RGB_SET_COLOR, b1, b2, b3, b4])

    def rgb_set_intensity(self, intensity):
        # Pack 8 bits into 7 bits
        b1 = intensity & 0x7F
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_RGB_SET_INTENSITY, b1])

    def potentiometer_read(self, callback):
        self._potentiometer_callback = callback
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_POTENTIOMETER_READ])

    def potentiometer_scale_to(self, to_low, to_high, callback):
        # Pack 14-bits into 2 7-bit bytes.
        to_low &= 0x3FFF
        l1 = to_low & 0x7F
        l2 = to_low >> 7

        # Pack 14-bits into 2 7-bit bytes.
        to_high &= 0x3FFF
        h1 = to_high & 0x7F
        h2 = to_high >> 7

        self._potentiometer_callback = callback
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_POTENTIOMETER_SCALE_TO, l1, l2, h1, h2])

    def ldr_read(self, callback):
        self._ldr_callback = callback
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_LDR_READ])

    def ldr_scale_to(self, to_low, to_high, callback):
        # Pack 14-bits into 2 7-bit bytes.
        to_low &= 0x3FFF
        l1 = to_low & 0x7F
        l2 = to_low >> 7

        # Pack 14-bits into 2 7-bit bytes.
        to_high &= 0x3FFF
        h1 = to_high & 0x7F
        h2 = to_high >> 7

        self._ldr_callback = callback
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_LDR_SCALE_TO, l1, l2, h1, h2])

    def ledmatrix_print(self, pattern):
        pattern[0] &= 0x7F
        pattern[1] &= 0x7F
        pattern[2] &= 0x7F
        pattern[3] &= 0x7F
        pattern[4] &= 0x7F

        self._command_handler.send_sysex(NPB_COMMAND, [NPB_LEDMATRIX_PRINT_PATTERN,
            pattern[0], pattern[1], pattern[2], pattern[3], pattern[4]])

    def ledmatrix_print_in_landscape(self, number):
        # Pack 8 bits into 7 bits
        b1 = number & 0x7F
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_LEDMATRIX_PRINT_IN_LAND, b1])

    def ledmatrix_print_char(self, symbol):
        # Pack 8 bits into 7 bits
        b1 = ord(symbol) & 0x7F
        self._command_handler.send_sysex(NPB_COMMAND, [NPB_LEDMATRIX_PRINT_CHAR, b1])

    def _parse_firmata_byte(self, data):
        """Parse a byte value from two 7-bit byte firmata response bytes."""
        if len(data) != 2:
            raise ValueError('Expected 2 bytes of firmata repsonse for a byte value!')
        return (data[0] & 0x7F) | ((data[1] & 0x01) << 7)

    def _parse_firmata_long(self, data):
        """Parse a 4 byte signed long integer value from a 7-bit byte firmata response
        byte array.  Each pair of firmata 7-bit response bytes represents a single
        byte of long data so there should be 8 firmata response bytes total.
        """
        if len(data) != 8:
            raise ValueError('Expected 8 bytes of firmata response for long value!')
        # Convert 2 7-bit bytes in little endian format to 1 8-bit byte for each
        # of the four long bytes.
        raw_bytes = bytearray(4)
        for i in range(4):
            raw_bytes[i] = self._parse_firmata_byte(data[i*2:i*2+2])
        # Use struct unpack to convert to long value.
        return struct.unpack('<l', raw_bytes)[0]

    def _parse_firmata_uint16(self, data):
        """Parse a 2 byte unsigned integer value from a 7-bit byte firmata response
        byte array.  Each pair of firmata 7-bit response bytes represents a single
        byte of int data so there should be 4 firmata response bytes total.
        """
        if len(data) != 4:
            raise ValueError('Expected 4 bytes of firmata response for int value!')
        # Convert 2 7-bit bytes in little endian format to 1 8-bit byte for each
        # of the two unsigned int bytes.
        raw_bytes = bytearray(2)
        for i in range(2):
            raw_bytes[i] = self._parse_firmata_byte(data[i*2:i*2+2])
        # Use struct unpack to convert to unsigned short value.
        return struct.unpack('<H', raw_bytes)[0]

    def _response_handler(self, data):
        # Callback invoked when a nanoplayboard sysex command is received.
        logger.debug('CP response: 0x{0}'.format(hexlify(bytearray(data))))

        print('CP response: 0x{0}'.format(hexlify(bytearray(data))))

        if len(data) < 1:
            logger.warning('Received response with no data!')
            return

        # Check what type of response has been received.
        command = data[0] & 0x7F

        if command == NPB_POTENTIOMETER_READ or command == NPB_POTENTIOMETER_SCALE_TO:
            # Parse potentiometer response
            if len(data) < 6:
                logger.warning('Received potentiometer response with not enough data!')
                return

            pot_value = self._parse_firmata_uint16(data[2:6])
            if self._potentiometer_callback is not None:
                self._potentiometer_callback(pot_value)

        elif command == NPB_LDR_READ or command == NPB_LDR_SCALE_TO:
            # Parse ldr response
            if len(data) < 6:
                logger.warning('Received ldr response with not enough data!')
                return

            ldr_value = self._parse_firmata_uint16(data[2:6])
            if self._ldr_callback is not None:
                self._ldr_callback(ldr_value)

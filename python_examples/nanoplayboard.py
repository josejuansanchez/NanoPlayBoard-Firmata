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

from PyMata.pymata import PyMata

CP_COMMAND           = 0x40  # Byte that identifies all NanoPlayBoard commands.
CP_BUZZER_PLAY_TONE  = 0x20  # Play a tone on the speaker. Sends next values:
                             #  - Frequency (hz). 2 7-bit bytes
                             #    (up to 2^14 hz, about 16khz)
                             #  - Duration (ms). 2 7-bit bytes
                             #    (up to 2^14 ms, about 16s)
CP_BUZZER_STOP_TONE  = 0x21  # Stop playing anything on the speaker.

CP_RGB_ON            = 0x03
CP_RGB_OFF           = 0x31
CP_RGB_TOGGLE        = 0x32
CP_RGB_SETCOLOR      = 0x33
CP_RGB_SETINTENSITY  = 0x34

class NanoPlayBoard(PyMata):
    def __init__(self, port_id='/dev/ttyACM0', bluetooth=True, verbose=True):
        PyMata.__init__(self, port_id, bluetooth, verbose)
        self._command_handler.command_dispatch.update({CP_COMMAND: [self._response_handler, 1]})

    def play_tone(self, frequency_hz, duration_ms=0):
        # Note:
        # 0x3FFF = 0011 1111 1111 1111
        # 0x7F   =           0111 1111

        # Pack 14-bits into 2 7-bit bytes.
        frequency_hz &= 0x3FFF
        f1 = frequency_hz & 0x7F
        f2 = frequency_hz >> 7
        
        # Again pack 14-bits into 2 7-bit bytes.
        duration_ms &= 0x3FFF
        d1 = duration_ms & 0x7F
        d2 = duration_ms >> 7
        self._command_handler.send_sysex(CP_COMMAND, [CP_BUZZER_PLAY_TONE, f1, f2, d1, d2])

    def stop_tone(self):
        self._command_handler.send_sysex(CP_COMMAND, [CP_BUZZER_STOP_TONE])

    def rgb_on(self):
        self._command_handler.send_sysex(CP_COMMAND, [CP_RGB_ON])

    def rgb_off(self):
        self._command_handler.send_sysex(CP_COMMAND, [CP_RGB_OFF])

    def rgb_toggle(self):
        self._command_handler.send_sysex(CP_COMMAND, [CP_RGB_TOGGLE])

    def rgb_set_color(self, red, green, blue):
        red &= 0xFF
        green &= 0xFF
        blue &= 0xFF
        b1 = red >> 1
        b2 = ((red & 0x01) << 6) | (green >> 2)
        b3 = ((green & 0x03) << 5) | (blue >> 3)
        b4 = (blue & 0x07) << 4
        self._command_handler.send_sysex(CP_COMMAND, [CP_RGB_SETCOLOR, b1, b2, b3, b4])

    def rgb_set_intensity(self, intensity):
        # Pack 8 bits into 7 bits
        b1 = intensity & 0x7F
        self._command_handler.send_sysex(CP_COMMAND, [CP_RGB_SETINTENSITY, b1])

    def _response_handler(self, data):
        print(data)
# NanoPlayBoard PyMata helper class.
#
# This is not an example, rather it's a class to add NanoPlayBoard-specific
# commands to PyMata.  Make sure this file is in the same directory as the
# examples!
#
# This class is based on the circuitplayground.py developed by: Tony DiCola
#
#  Copyright (C) 2016 Tony DiCola.  All rights reservered.
#  Copyright (C) 2016 Jose Juan Sanchez.  All rights reservered.
#
# Licensed under the GNU General Public License, Version 3 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.gnu.org/licenses/gpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from PyMata.pymata import PyMata

CP_COMMAND  = 0x40  # Byte that identifies all NanoPlayBoard commands.
CP_TONE     = 0x20  # Play a tone on the speaker, expects the following bytes as data:
                    #  - Frequency (hz) as 2 7-bit bytes (up to 2^14 hz, or about 16khz)
                    #  - Duration (ms) as 2 7-bit bytes.
CP_NO_TONE  = 0x21  # Stop playing anything on the speaker.

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
        self._command_handler.send_sysex(CP_COMMAND, [CP_TONE, f1, f2, d1, d2])

    def stop_tone(self):
        self._command_handler.send_sysex(CP_COMMAND, [CP_NO_TONE])

    def _response_handler(self, data):
        print(data)
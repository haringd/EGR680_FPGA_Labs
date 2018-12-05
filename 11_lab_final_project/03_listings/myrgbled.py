#   Copyright (c) 2016, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#   edited by Dimitri Haring
#   date 12/04/2018

from pynq import MMIO
from pynq import PL
import time

__author__ = "Graham Schelle"
__copyright__ = "Copyright 2016, Xilinx"
__email__ = "pynq_support@xilinx.com"


RGBLEDS_XGPIO_OFFSET = 0
RGBLEDS_START_INDEX = 4
RGB_CLEAR = 0
RGB_BLUE = 1
RGB_GREEN = 2
RGB_CYAN = 3
RGB_RED = 4
RGB_MAGENTA = 5
RGB_YELLOW = 6
RGB_WHITE = 7


class MYRGBLED(object):
    """This class controls the onboard RGB LEDs.

    Attributes
    ----------
    index : int
        The index of the RGB LED, from 4 (LD4) to 5 (LD5).
    _mmio : MMIO
        Shared memory map for the RGBLED GPIO controller.
    _rgbleds_val : int
        Global value of the RGBLED GPIO pins.
        
    """
    _mmio = None
    _rgbleds_val = 0

    def __init__(self, index):
        """Create a new RGB LED object.
        
        Parameters
        ----------
        index : int
            Index of the RGBLED, from 4 (LD4) to 5 (LD5).
        
        """
        # print("Changed LED Driver to MYRGBLED.") # debugging only
        if index not in [4, 5]:
            raise ValueError("Index for onboard RGBLEDs should be 4 or 5.")
            
        self.index = index
        if MYRGBLED._mmio is None:
            base_addr = PL.ip_dict["rgbleds_gpio"]["phys_addr"]
            MYRGBLED._mmio = MMIO(base_addr, 16)

    def on(self, color):
        """Turn on a single RGB LED with a color value (see color constants).
        
        Parameters
        ----------
        color : int
           Color of RGB specified by a 3-bit RGB integer value.
        
        Returns
        -------
        None
        
        """
        if color not in range(8):
            raise ValueError("color should be an integer value from 0 to 7.")

        rgb_mask = 0x7 << ((self.index-RGBLEDS_START_INDEX)*3)
        new_val = (MYRGBLED._rgbleds_val & ~rgb_mask) | \
                  (color << ((self.index-RGBLEDS_START_INDEX)*3))
        self._set_rgbleds_value(new_val)
        
    def off(self):
        """Turn off a single RGBLED.
        
        Returns
        -------
        None
        
        """
        rgb_mask = 0x7 << ((self.index-RGBLEDS_START_INDEX)*3)
        new_val = MYRGBLED._rgbleds_val & ~rgb_mask
        self._set_rgbleds_value(new_val)
        
    def red_on(self):
        """Turn on a single RGB LED with color value red.
        
        Parameters
        ----------
        color : int
           Color of RGB specified by a 3-bit RGB integer value.
        
        Returns
        -------
        None
        
        """
#        if color not in range(8):
#            raise ValueError("color should be an integer value from 0 to 7.")
        new_val = (MYRGBLED._rgbleds_val ) | (RGB_RED << ((self.index-RGBLEDS_START_INDEX)*3))
#        print(MYRGBLED._rgbleds_val)
#        print(new_val)
#        print( (RGB_RED << ((self.index-RGBLEDS_START_INDEX)*3)) )
        self._set_rgbleds_value(new_val)
        
    def red_off(self):
        """Turn off a single RGB LED with color value red.
        
        Parameters
        ----------
        color : int
           Color of RGB specified by a 3-bit RGB integer value.
        
        Returns
        -------
        None
        
        """
#        if color not in range(8):
#            raise ValueError("color should be an integer value from 0 to 7.")

        new_val = (MYRGBLED._rgbleds_val ) &~ (RGB_RED << ((self.index-RGBLEDS_START_INDEX)*3))                 
        self._set_rgbleds_value(new_val)
        
    def green_on(self):
        """Turn on a single RGB LED with color value green.
        
        Parameters
        ----------
        color : int
           Color of RGB specified by a 3-bit RGB integer value.
        
        Returns
        -------
        None
        
        """
#        if color not in range(8):
#            raise ValueError("color should be an integer value from 0 to 7.")

        new_val = (MYRGBLED._rgbleds_val ) | (RGB_GREEN << ((self.index-RGBLEDS_START_INDEX)*3))
        self._set_rgbleds_value(new_val)
        
    def green_off(self):
        """Turn off a single RGB LED with color value green.
        
        Parameters
        ----------
        color : int
           Color of RGB specified by a 3-bit RGB integer value.
        
        Returns
        -------
        None
        
        """
#        if color not in range(8):
#            raise ValueError("color should be an integer value from 0 to 7.")

        new_val = (MYRGBLED._rgbleds_val ) &~ (RGB_GREEN << ((self.index-RGBLEDS_START_INDEX)*3))                 
        self._set_rgbleds_value(new_val)
        
    def blue_on(self):
        """Turn on a single RGB LED with color value blue.
        
        Parameters
        ----------
        color : int
           Color of RGB specified by a 3-bit RGB integer value.
        
        Returns
        -------
        None
        
        """
#        if color not in range(8):
#            raise ValueError("color should be an integer value from 0 to 7.")

        new_val = (MYRGBLED._rgbleds_val ) | (RGB_BLUE << ((self.index-RGBLEDS_START_INDEX)*3))
        self._set_rgbleds_value(new_val)
        
    def blue_off(self):
        """Turn off a single RGB LED with color value blue.
        
        Parameters
        ----------
        color : int
           Color of RGB specified by a 3-bit RGB integer value.
        
        Returns
        -------
        None
        
        """
#        if color not in range(8):
#            raise ValueError("color should be an integer value from 0 to 7.")

        new_val = (MYRGBLED._rgbleds_val ) &~ (RGB_BLUE << ((self.index-RGBLEDS_START_INDEX)*3))                 
        self._set_rgbleds_value(new_val)

    def status(self):
        rgb_mask = 0x7 << ((self.index-RGBLEDS_START_INDEX)*3)
        return ((MYRGBLED._rgbleds_val )& ~rgb_mask)
    
    def rgb_on(self, color):
        """Turn on a single RGB LED color.
        
        Parameters
        ----------
        color : int
           Color of RGB specified by a 3-bit RGB integer value.
               Blue  = 1
               Green = 2
               Red = 4
        
        Returns
        -------
        None
        
        """
        if color not in [1, 2, 4]:
            raise ValueError("color should be an integer value from 1, 2, and 4.")

        new_val = (MYRGBLED._rgbleds_val ) | (color << ((self.index-RGBLEDS_START_INDEX)*3))
        self._set_rgbleds_value(new_val)
        
    def rgb_off(self, color):
        """Turn off a single RGB LED color.
        
        Parameters
        ----------
        color : int
           Color of RGB specified by a 3-bit RGB integer value.
               Blue  = 1
               Green = 2
               Red = 4
        Returns
        -------
        None
        
        """
        if color not in [1, 2, 4]:
            raise ValueError("color should be an integer value from 1, 2, and 4.")

        new_val = (MYRGBLED._rgbleds_val ) &~ (color << ((self.index-RGBLEDS_START_INDEX)*3))                 
        self._set_rgbleds_value(new_val)

    def pwm(self, color, duty_cycle, frequency):
		"""PWM for single RGB LED color.
	
		Parameters
		----------
		color : int 1, 2 or 3
			Color of RGB specified by a 3-bit RGB integer value.
				Blue  = 1
				Green = 2
				Red = 4
		duty_cycle : int between 0 and 100
			Duty cycle is an integer value between 0 and 100 %
			____+----+____+----+____+ is a duty cyle of 50 %
		frequency : int
			Frequency defines the length of the intervall

        Returns
        -------
        None
        
        """        
        if color not in [1, 2, 4]:
            raise ValueError("color should be an integer value from 1, 2, and 4.")

        self.rgb_on(color)
        time.sleep( duty_cycle / frequency )
        self.rgb_off(color)
        time.sleep( (100-duty_cycle) / frequency)                 
        
    def write(self, color):
        """Set the RGBLED state according to the input value.

        Parameters
        ----------
        color : int
            Color of RGB specified by a 3-bit RGB integer value.
            
        Returns
        -------
        None
        
        """
        self.on(color)

    def read(self):
        """Retrieve the RGBLED state.

        Returns
        -------
        int
            The color value stored in the RGBLED.
            
        """
        return (MYRGBLED._rgbleds_val >> 
                ((self.index-RGBLEDS_START_INDEX)*3)) & 0x7

    @staticmethod
    def _set_rgbleds_value(value):
        """Set the state of all RGBLEDs.
        
        Note
        ----
        This function should not be used directly. User should call 
        `on()`, `off()`, instead.
        
        Parameters
        ----------
        value : int 
            The value of all the RGBLEDs encoded in a single variable.
        
        """
        MYRGBLED._rgbleds_val = value
        MYRGBLED._mmio.write(RGBLEDS_XGPIO_OFFSET, value)

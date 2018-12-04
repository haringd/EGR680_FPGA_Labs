
# coding: utf-8

# # Part II - LED Groove Bar
# Demonstrates how the LED Groove Bar level is set with slider SL1. The brightness can be chosen in four levels with slider SL2.
# 
# LED Bar Brightness
#  - 0 = off
#  - 1 = low
#  - 2 = medium
#  - 3 = hight 

# In[2]:


# Steup the PYNQ board
from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")

from pynq.lib.pmod import Grove_LEDbar
from pynq.lib.pmod import PMOD_GROVE_G1 # Import constants
import ipywidgets as widgets
from IPython.display import display

# For delays
from time import sleep

# Global values
g_ledBrightness  = 3
g_leds = 0

# defined functions
def handle_slider1_change(change):
    global g_leds
    ledbar.write_level(change.new, g_ledBrightness, 1)
    g_leds = change.new
def handle_slider2_change(change):
    global g_ledBrightness
    g_ledBrightness = change.new
    ledbar.write_level(g_leds, change.new, 1)
   # ledbar.write_brightness(ledbar.read(), change.new)


# Instantiate Grove LED Bar on PMODA and on Pmod2Grove G1
ledbar = Grove_LEDbar(base.PMODA, PMOD_GROVE_G1)
ledbar.reset()

# Flash 2 extreme LEDs of the LED Bar in a loop, dubbiging only
# for i in range(5):
#     ledbar.write_binary(0b1000000001)
#     sleep(0.5)
#     ledbar.write_binary(0b0000000000)
#     sleep(0.5)

# GUI 
slider1 = widgets.IntSlider(min=0, max=10, value=0, description='SL1')
slider2 = widgets.IntSlider(min=0, max=3, value=0, description='SL2')

slider1.observe(handle_slider1_change, names='value')
slider2.observe(handle_slider2_change, names='value')

display(slider1, slider2)


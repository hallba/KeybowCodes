# SPDX-FileCopyrightText: 2021 Sandy Macdonald
#
# SPDX-License-Identifier: MIT

# A simple example of how to set up a keymap and HID keyboard on Keybow 2040.

# You'll need to connect Keybow 2040 to a computer, as you would with a regular
# USB keyboard.

# Drop the keybow2040.py file into your `lib` folder on your `CIRCUITPY` drive.

# NOTE! Requires the adafruit_hid CircuitPython library also!

import board
from keybow2040 import Keybow2040

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# A map of keycodes that will be mapped sequentially to each of the keys, 0-15
keymap =    [Keycode.SHIFT,
             Keycode.C,
             Keycode.LEFT_ARROW,
             Keycode.Z,
             Keycode.RIGHT_SHIFT,
             Keycode.RIGHT_SHIFT,
             Keycode.DOWN_ARROW,
             Keycode.UP_ARROW,
             Keycode.RIGHT_SHIFT,
             Keycode.RIGHT_SHIFT,
             Keycode.RIGHT_ARROW,
             Keycode.SPACE,
             Keycode.RIGHT_SHIFT,
             Keycode.RIGHT_SHIFT,
             Keycode.RIGHT_SHIFT,
             Keycode.RIGHT_SHIFT]

# Th e  colour to set the keys when pressed, cyan.
cyan = (0, 255, 255)
purple = (153, 102, 255)
green = (51, 204, 0)
white = (200, 200, 255)
yellow = (255, 255, 0)
orange = (255, 55, 0)
pink = (255, 102, 204)

colourMap = [
            green,
            cyan,
            white,
            cyan,
                    green,
                    orange,
                    white,
                    white,
                            green,
                            cyan,
                            white,
                            orange,
                                    green,
                                    cyan,
                                    cyan,
                                    cyan
            ]

holdStatus = [ False for _ in range(16)]

# Attach handler functions to all of the keys
for index, key in enumerate(keys):
    # A press handler that sends the keycode and turns on the LED
    @keybow.on_press(key)
    def press_handler(key):
        keycode = keymap[key.number]
        keyboard.send(keycode)
        key.set_led(*pink)
        holdStatus[index] = True

    # A release handler that turns off the LED
    @keybow.on_release(key)
    def release_handler(key):
        rgb = colourMap[key.number]
        key.set_led(*rgb)
        #key.led_off()
        holdStatus[index] = False

    # A hold handler
    @keybow.on_hold(key)
    def hold_handler(key):
        keycode = keymap[key.number]
        keyboard.send(keycode)
        key.set_led(*purple)

for key in keys:
    rgb = colourMap[key.number]
    key.set_led(*rgb)
    if key.number != 3:
        key.hold_time = 0.1

while True:
    # Always remember to call keybow.update()!
    keybow.update()
    for key in keys:
        if key.held:
            keycode = keymap[key.number]
            keyboard.send(keycode)

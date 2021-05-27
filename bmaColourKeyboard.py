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

import time

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# bma colours - pink, orange, green, mint, purple, membrane protein blue, 
# cell blue, ec grey, ec orange, ec green, ec mint, ec purple
bmaColours =  [ (255, 102, 204), 
                (255, 153, 0), 
                (51, 204, 0), 
                (0, 204, 204), 
                (153, 102, 255),

                (51, 153, 204),

                (208, 233, 240),
                
                (204, 204, 204),
                (255, 204, 153), 
                (171, 255, 171),
                (125, 244, 235),
                (204, 204, 255)
                ]

white = 255, 255, 255
realWhite = 185, 191, 200
#Bma colours as projected
ledColours = [
    (142, 97, 239),
    (255, 195, 118),
    (107, 228, 123),
    (0, 255, 254),
    (205, 69, 255),
    (45, 105, 242),
    (200, 176, 255),
    (223, 195, 255),
    (223, 161, 241),
    (134, 149, 228),
    (128, 168, 255),
    (158, 158, 229)
]
ledHighlights = [
    (246, 0, 233),
    (255, 187, 137),
    (0, 255, 155),
    (0, 255, 155),
    (126, 0, 255),
    (0, 255, 255),
    (189, 144, 255),
    (194, 192, 255),
    (223, 158, 191),
    (160, 255, 255),
    (185, 255, 255),
    (173, 166, 255)
]

# bma highlights 
bmaHighlights = [ (153, 0, 102), 
                  (255, 102, 0), 
                  (0, 102, 0), 
                  (0, 102, 102), 
                  (51, 0, 153), 

                  (0, 51, 102),

                  (98, 185, 209),

                  (124, 124, 124),
                  (249, 151, 70),
                  (92, 224, 92),
                  (82, 198, 184),
                  (139, 139, 252)
                ]
# Th e  colour to set the keys when pressed, cyan.
cyan = (0, 255, 255)
purple = (153, 102, 255)
#green = (51, 204, 0)
white = (200, 200, 255)
yellow = (255, 255, 0)
orange = (255, 55, 0)
pink = (255, 102, 204)
red = (255, 0, 0)
blue = (0, 0 ,255)
green = (0, 255, 0)
black = None

colourMap = [
            None,
            8,
            4,
            0,
                    None,
                    9,
                    5,
                    1,
                            None,
                            10,
                            6,
                            2,
                                    None,
                                    11,
                                    7,
                                    3
            ]

def coordinateToArray(x,y):
    # assumes cable is at top
    if x>3 or y>3 or x<0 or y <0:
        return(None)
    else:
        return(y+x*4)

def indexToCoordinates(i):
    if i<0 or i>15:
        return(None)
    else:
        return(i/4,i%4)

def enforceColourRange(rgb):
    r, g, b = rgb
    def rangeProtect(x):
        if x > 255: 
            cx = 255
        elif x<0:
            cx = 0
        else:
            cx = x
        return(cx)
    return((rangeProtect(r), rangeProtect(g), rangeProtect(b)))
    
    

def calibrateColour(rgb):
    r, g, b = rgb
    #Calibrations from photo in daylight
    '''
    cR = int((r - 47)/0.77)
    cG = int((g - 97)/0.49)
    cB = int((b - 158)/0.44)
    '''
    #Calibrations from photo in dark
    '''
    cR = int((r - 46)/0.88)
    cG = int((g - 86)/0.70)
    cB = int((b - 129)/0.64)
    '''
    #Manual estimation
    
    cR = int((r-50)/0.95)
    cG = int((g - 75)/0.92)
    cB = int((b-50)/0.95)
    
    #Simple range adjustment
    '''
    def squash(low, high, value):
        #Value ranges from 0 to 255, squashed into the range low to high
        scale = (high-low)/255
        return(int(value*scale)+low)
    cR = squash(70,200,r)
    cG = squash(70,200,g)
    cB = squash(70,200,b)
    '''
    #print(cR,cG,cB)
    result = enforceColourRange((cR, cG, cB))
    return(result)
    
def reportCalibration():
    for i,(c,h) in enumerate(zip(bmaColours,bmaHighlights)):
        print(i)
        print("I",c,h)
        print("O",calibrateColour(c),calibrateColour(h))

holdStatus = [ False for _ in range(16)]

'''
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
'''

def darken(rgb, factor):
    r, g, b = rgb
    def intScale(x):
        return(int(x/factor))
    result = (intScale(r), intScale(g), intScale(b))
    return(result)


modifier = [False,False]

def draw():
    for key in keys:
        colour = colourMap[key.number]
        if colour == None:
            key.led_off()
        else:
            if not modifier[0]:
                rgb = calibrateColour(bmaColours[colour])
            else:
                rgb = calibrateColour(bmaHighlights[colour])
            key.led_on()
            key.set_led(*rgb)

draw()

highlight = keys[0]

@keybow.on_press(highlight)
def press_handler(key):
    modifier[0]=True
    draw()
    key.set_led(*cyan)
    key.led_on()

@keybow.on_release(highlight)
def release_handler(key):
    modifier[0]=False
    draw()
    key.led_off()

rgbKey = keys[4]
rgbKey.set_led(*red)
rgbState = 0
@keybow.on_press(rgbKey)
def press_handler(key):
    modifier[1]=True
    draw()
    key.led_off()

@keybow.on_release(rgbKey)
def release_handler(key):
    modifier[1]=False
    draw()
    key.led_on()

lastTime = time.monotonic()

def rgbToHex(rgb):
    return('%02x%02x%02x' % rgb)

# Handlers for colour keys. Modifier returns rgb rather than hex

pink = keys[3]

def colourPrintGeneric(key, colourID):
    key.led_off()
    if not modifier[0]:
        colour=bmaColours[colourID]
    else:
        colour=bmaHighlights[colourID]
    if not modifier[1]:
        result=rgbToHex(colour)
        #Have to do a bit of extra work to print the # on a mac
        keyboard.press(Keycode.ALT)
        keyboard.press(Keycode.THREE)
        keyboard.release_all()
    else:
        result=str(colour)
    layout.write(result)

for key in keys:
    if colourMap[key.number] == None:
        continue
    @keybow.on_press(key)
    def press_handler(key):
        colourPrintGeneric(key, colourMap[key.number])

    @keybow.on_release(key)
    def release_handler(key):
        key.led_on()

while True:
    # Always remember to call keybow.update()!
    keybow.update()

    time_elapsed = time.monotonic() - lastTime
    if time_elapsed > 2 and not modifier[1]:
        if rgbState == 0:
            rgbState += 1
            rgbKey.set_led(*green)
        elif rgbState == 1:
            rgbState += 1
            rgbKey.set_led(*blue)
        else:
            rgbState = 0
            rgbKey.set_led(*red)
        lastTime = time.monotonic()


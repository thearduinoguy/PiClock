#!/usr/bin/env python
"""This programme displays the date and time on an RGBMatrix display."""

import time
import datetime
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix


# Load up the font (use absolute paths so script can be invoked
# from /etc/rc.local correctly)
def loadFont(font):
    global fonts
    fonts[font] = graphics.Font()
    fonts[font].LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/" + font + ".bdf")

flip = True
tick = True
scroller = 64

# init the RGB matrix as 32 Rows, 2 panels (represents 32 x 64 panel), 1 chain
MyMatrix = RGBMatrix(32, 2, 1)

# Bits used for PWM. Something between 1..11. Default: 11
MyMatrix.pwmBits = 8

# Sets brightness level. Default: 100. Range: 1..100"
MyMatrix.brightness = 75

# set colour
ColorWHI = graphics.Color(255, 255, 255)
RED = graphics.Color(255, 0, 0)
GREEN = graphics.Color(0, 255, 0)
BLUE = graphics.Color(0, 0, 255)
YELLOW = graphics.Color(255, 255, 0)
PURPLE = graphics.Color(255, 0, 255)

lastDateFlip = int(round(time.time() * 1000))
lastSecondFlip = int(round(time.time() * 1000))
lastScrollTick = int(round(time.time() * 1000))

fonts = {}

loadFont('7x13B')
loadFont('9x18B')
loadFont('6x9')

# Create the buffer canvas
MyOffsetCanvas = MyMatrix.CreateFrameCanvas()
while(1):
    currentDT = datetime.datetime.now()

    if currentDT.hour < 23:
        scrollColour = BLUE
        fulldate = currentDT.strftime("%d-%m-%y  %A")
        if currentDT.day < 10:
            fulldate = fulldate[1:]
    else:
        scrollColour = PURPLE
        fulldate = "GO HOME!!!"

    sizeofdate = len(fulldate)*7

    Millis = int(round(time.time() * 1000))

    if Millis-lastSecondFlip > 1000:
        lastSecondFlip = int(round(time.time() * 1000))
        tick = not tick

    if Millis-lastDateFlip > 5000:
        lastDateFlip = int(round(time.time() * 1000))
        flip = not flip

    scroller = scroller-1
    if scroller == (-sizeofdate):
        scroller = 64

    thetime = currentDT.strftime("%l"+(":" if tick else " ")+"%M")

    thetime = str.lstrip(thetime)
    sizeoftime = (25 - (len(thetime) * 9) / 2)

    # theday = currentDT.strftime("%A")
    # sizeofday = (32 - (len(theday)* 7)/2)

    pmam = currentDT.strftime("%p")

    graphics.DrawText(MyOffsetCanvas, fonts['7x13B'], scroller, 28,
                      scrollColour, fulldate)

    graphics.DrawText(MyOffsetCanvas, fonts['9x18B'], sizeoftime, 14, RED,
                      thetime)

    graphics.DrawText(MyOffsetCanvas, fonts['6x9'], 50, 14, GREEN, pmam)

    MyOffsetCanvas = MyMatrix.SwapOnVSync(MyOffsetCanvas)
    MyOffsetCanvas.Clear()
    time.sleep(0.05)

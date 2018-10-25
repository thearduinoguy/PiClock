#!/usr/bin/env python
"""This programme displays the date and time on an RGBMatrix display."""

import time
import datetime
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix

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


# Create the buffer canvas
MyOffsetCanvas = MyMatrix.CreateFrameCanvas()
while(1):
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13B.bdf")

    currentDT = datetime.datetime.now()

    fulldate = currentDT.strftime("%d-%m-%y  %A")
    if currentDT.day < 10:
        fulldate = fulldate[1:]

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

    graphics.DrawText(MyOffsetCanvas, font, scroller, 28, BLUE, fulldate)

    # Load up the font (use absolute paths so script can be invoked
    # from /etc/rc.local correctly)

    graphics.DrawText(MyOffsetCanvas, font, scroller, 28, BLUE, fulldate)

    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/9x18B.bdf")
    graphics.DrawText(MyOffsetCanvas, font, sizeoftime, 14, RED, thetime)

    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x9.bdf")
    graphics.DrawText(MyOffsetCanvas, font, 50, 14, GREEN, pmam)

    MyOffsetCanvas = MyMatrix.SwapOnVSync(MyOffsetCanvas)
    MyOffsetCanvas.Clear()

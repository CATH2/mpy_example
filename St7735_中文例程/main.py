from machine import SPI,Pin,PWM
import st7735
import time,random
from bmpdecoder import bmpFileData

def initDisplay(rotate = True):
    global display,tftVdd
    tftVdd = PWM(Pin(11),freq =1000,duty = 500)
    display = st7735.TFT(
        SPI(1,baudrate=60000000, polarity=0, phase=0,
            sck=Pin(2),mosi=Pin(3),miso=Pin(10)),
        6,10,7)#spi, aDC, aReset, aCS,ScreenSize = (160, 160)
    display.initr()
    display.invertcolor(False)
    if rotate:
        display.rotation(2)
        #display._offset = (26,1)#(26,1)
    else:
        display.rotation(1)
        #display._offset = (1,26)#(26,1)
    display.fill(0)
    
initDisplay()

import zhFont2tft as font

tftfont = font.Font16('font1616.ebin')
tftfont.text(0,0,'111111111',display,color = [0,255,0],backgroundcolor = [0,0,0],linecount = 8)
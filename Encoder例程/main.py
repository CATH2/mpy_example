from encoder import Encoder
from machine import Pin,PWM,SPI
from sh1106 import SH1106_SPI
from sprite import DataDisplayScreen
from EC11 import EC11
led0 = PWM(Pin(12),freq = 200000,duty = 0)
led1 = PWM(Pin(13),freq = 200000,duty = 0)
# 
e = Encoder(0,1,Pin.PULL_UP,max_val=100,min_val=-100)
eButton = Pin(3,Pin.IN,pull = Pin.PULL_UP)
spi = SPI(1, 8000000, sck=Pin(5), mosi=Pin(11))
display = SH1106_SPI(128,64,spi,dc=Pin(6),res=Pin(7),cs = Pin(10), rotate=180)
dds1 = DataDisplayScreen(y = 40,delta = 1,height = 0.5)
def show():
    dds1.draw(display)
    display.show()
value = 0
while True:
#     display.fill(0)
    if e.value < value:
        print('---')
    display.text(str(e.value),0,0)
    if not eButton.value():
        display.text("Button",0,8)
    dds1+e.value
    value = e.value
#     print(e.value)
#     dds2+ea.value()
    show()
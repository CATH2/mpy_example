import network
import time
wlan = network.WLAN(network.STA_IF)
def Connect():#链接wifi
    global wlan
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('PRATO', 'a2125746')
        i = 1
        while not wlan.isconnected():
            print("正在连接...{}".format(i))
            i += 1
            time.sleep(1)
            if i > 10:
                print('异常')
                return False
    print('network config:', wlan.ifconfig())
    return True

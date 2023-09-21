import time, network


def wifi_connect(ssid,password,led=None):
    # 创建 WIFI 连接对象
    wlan = network.WLAN(network.STA_IF)
    # 激活接口
    wlan.active(True)
    # 断开之前的连接
    wlan.disconnect()
    # 扫描允许访问的WIFI
    print('扫描周围信号源:',wlan.scan())
    # 连接WIFI
    print("正在连接WIFI",end='')
    wlan.connect(ssid,password)
    maxTime = 50
    # 判断是否连接成功
    while not wlan.isconnected():
        if led:led.value(not led.value())
        print('.',end='')
        time.sleep(0.3)
        maxTime -= 1
        if maxTime == 0:
            print("连接失败")
            break
    if maxTime != 0:print('\n连接成功！')
    return wlan


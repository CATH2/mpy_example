import network

station = network.WLAN(network.STA_IF)

def connect(sid,psd):
    global station
    ssid = sid
    password = psd
    
    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
      pass
     
    print('连接成功')
    print(station.ifconfig())

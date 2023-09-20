import umqtt as mqtt
import wifi
from machine import Timer

def HeartBeating(t):
    global clinet
    try:
        client.ping()
    except Exception as e:
        print(e)
        try:
            client.connect(False)
        except Exception as e:
            print("error code 0")
            t.deinit()
def MqttCallback(topic,msg):
    global g
    print(topic,msg)

wifi.Connect()
# id address port 用户名 密码 心跳时间
client = mqtt.MQTTClient("esp32_123","z35620v638.zicp.fun", port=40916, user="test", password="666555",keepalive=10)
#10*1.5 = 15s
#ip 1883 
client.connect(False)
clientHeartBeating = Timer(0)
clientHeartBeating.init(period=5000, mode=Timer.PERIODIC, callback=HeartBeating)
client.set_callback(MqttCallback)
client.subscribe("test2")

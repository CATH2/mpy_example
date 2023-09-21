"""
说明：LED显示配网状态
LED一长一短闪烁：进入配网模式
LED闪烁：表示正在尝试连接网络。
LED常亮：表示网络连接成功
LED常灭：表示等待配网
LED闪烁5次：表示已清除wifi信息
用户操作：
# 手机连接 2.4G 无线网络（重要）
# 关注 安信可科技 微信公众号，点击 应用开发→微信配网，或
# 关注 乐鑫信息科技 微信公众号，点击 商铺→Airkiss 设备，或
# 安装 EspTouch app，点击 EspTouch，或
# 安装 腾讯连连 app，任意添加一个设备
# 输入 Wi-Fi密码 后点击 连接按钮
"""
from utime import sleep
import network
import socket
import smartconfig
import _thread
from common.wifi import wifi_connect
from machine import Pin
import ujson


class SC:
    def __init__(self):
        self.pin2 = Pin(2, Pin.OUT)
        self.pin2.value(0)  # 熄灭等待连接

    def start_smartconfig(self):
        network.WLAN(network.STA_IF).active(True)
        smartconfig.start()
        # 启动一个新线程来检测smartconfig是否成功
        _thread.start_new_thread(self.check_smartconfig, ())

    def check_smartconfig(self):
        print("wait smartconfig connect")
        long = True
        while not smartconfig.success():
            print(".", end="")
            if self.pin2.value() == 0:
                self.pin2.value(1)
                if long:
                    sleep(1)
                    long = False
                else:
                    sleep(0.3)
                    long = True
            else:
                self.pin2.value(0)
            sleep(0.1)

        # 当smartconfig成功时执行相应操作
        self.on_smartconfig_success()

    def on_smartconfig_success(self):
        self.ssid, self.password, self.sc_type, self.token = smartconfig.info()
        print("receive data：", smartconfig.info())
        self.wlan = wifi_connect(self.ssid, self.password, self.pin2)
        if self.wlan.isconnected():
            self.pin2.value(1)  # 常亮表示连接成功
            print("smartconfig success and wifi connect success")
            # 以下代码用于保存配网信息
            # 数据示例
            with open("config.json", "r") as json_file:
                data = ujson.load(json_file)
            data["smartconfig"] = {
                "ssid": self.ssid,
                "pwd": self.password,
            }

            # 将数据写入JSON文件
            with open("config.json", "w") as json_file:
                ujson.dump(data, json_file)

            # 以下代码用于向手机发送配网完成通知，可选项
            self.send_ack(self.wlan.ifconfig()[0], self.wlan.config("mac"))
        else:
            self.pin2.value(0)  # 熄灭表示连接失败

    def inet_pton(self, ip_str: str):
        """将字符串 IP 地址转换为字节串"""
        ip_bytes = b""
        ip_segs = ip_str.split(".")

        for seg in ip_segs:
            ip_bytes += int(seg).to_bytes(1, "little")

        return ip_bytes

    def send_ack(self, local_ip, local_mac):
        """向手机发送配网完成通知"""
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        data = smartconfig.info()[2].to_bytes(1, "little") + local_mac
        port = 10000  # airkiss 端口号

        if smartconfig.info()[3] == smartconfig.TYPE_ESPTOUCH:
            data += self.inet_pton(local_ip)
            port = 18266  # esptouch 端口号

        for _ in range(30):
            sleep(0.1)
            try:
                udp.sendto(data, ("255.255.255.255", port))
            except OSError:
                pass
        print("send end")


if __name__ == "__main__":
    # 从JSON文件中读取数据
    with open("config.json", "r") as json_file:
        data = ujson.load(json_file)
    wifiInfo = data.get("smartconfig")
    flag = True
    if wifiInfo:
        ssid, pwd = wifiInfo.get("ssid"), wifiInfo.get("pwd")
        print("connecting to:", "ssid:", ssid, "pwd:", pwd)
        wlan = wifi_connect(ssid, pwd,Pin(2,Pin.OUT))
        if wlan.isconnected():
            print("wifi connect success")
            flag = False
        else:
            print("wifi connect fail")
            data["smartconfig"] = None
            # 将数据写入JSON文件
            with open("config.json", "w") as json_file:
                ujson.dump(data, json_file)
    if flag:
        Sc = SC()
        Sc.start_smartconfig()
    

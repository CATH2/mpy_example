import Wifi,uemail,ujson
Wifi.ConnectWifi()
#接收邮件服务器：imap.qq.com，使用SSL，端口号993
#发送邮件服务器：smtp.qq.com，使用SSL，端口号465或587
smtp = uemail.SMTP('smtp.qq.com', 587,
                  username='邮箱地址',
                  password='授权码')
smtp.to('1343482347@qq.com')
smtp.write("Subject:标题\n")
smtp.write("""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:Orange;">发送自Micropython</h1>
    </body>
</html>
""")
smtp.send()
smtp.quit()
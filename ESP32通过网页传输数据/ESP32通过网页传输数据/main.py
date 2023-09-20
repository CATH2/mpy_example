import socket
import _thread,gc
import time

# 数据采集中
connect('','')
web_page = open('index.html').read()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((station.ifconfig()[0], 80))
s.listen(2)

i=0
def add_01():
    global i 
    i+=1
    time.sleep(1)
def app():
    global web_page,s,i
    while True:
        try:
            print('waiting\n\r')
            if gc.mem_free() < 102000:
                gc.collect()
            conn, addr = s.accept()
            conn.settimeout(3.0)
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            conn.settimeout(None)
            #request = str(request)
            #print('Content = %s' % request)
            index = web_page%(i,'采集中',0,0)
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(index)
            conn.close()
            i+=1
        except OSError as e:
            conn.close()
            print(e,'Connection closed')
_thread.start_new_thread(add_01, ()) 
_thread.start_new_thread(app, ()) 


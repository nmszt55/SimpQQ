from socket import *
from web.setting import *

def connect():
    import time
    time.sleep(3)
    stri = OTHER_HEAD["FILE_INF_HEAD"] + FILE_SEPARATE + "addr" + FILE_SEPARATE + "sendtest.jpg" + FILE_SEPARATE + \
           "sendid" + FILE_SEPARATE + "asdasddsaxzc11321bvc6132b1v32m132468t74h86" + END_SEPARATE
    file = "/home/tarena/下载/abc.jpg"

    with open(file, "rb") as f:
        print('开始传输文件')
        sock = socket()
        sock.connect(("localhost", 7895))
        sock.send(stri.encode())
        time.sleep(2)
        while True:
            data = f.read(1024)
            if not data:
                print("传输完成")
                sock.close()
                return
            sock.send(data)
connect()
'''
    主要功能:在聊天窗口创建,为了能够向服务器发送文件或者图片
'''

from socket import *
from web.setting import *
from time import sleep


class Filesocket(object):
    def __init__(self, fromid, toid, filename, maxdata, md5, type="send"):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.fromid = fromid
        self.toid = toid
        self.filename = filename
        self.md5 = md5
        self.maxdata = maxdata
        self.type = type

    def start(self):
        self.sock.connect((SER_HOST, SER_PORT))
        if self.type == "send":
            stri = OTHER_HEAD["THIS_IS_FILESOCK_HEAD"] + FILE_SEPARATE + self.fromid + FILE_SEPARATE + self.toid + \
                  FILE_SEPARATE + self.filename + FILE_SEPARATE + str(self.maxdata) + FILE_SEPARATE + self.md5
            self.sock.send(stri.encode(CHARSET))
            sleep(0.5)

        # 接收文件
        if self.type == "recv":
            stri = OTHER_HEAD["RECV_FILE_LOG"] + FILE_SEPARATE + self.filename

    def send_file(self, data, type="rb"):
        if type == "r":
            data = data.encode()
        self.sock.send(data)

    def close(self):
        print("sender close")
        self.sock.close()

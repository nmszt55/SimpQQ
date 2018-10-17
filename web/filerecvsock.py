from socket import *
from threading import Thread
import os
import signal
from web.setting import *
from PyQt5.QtCore import QThread


class recvSock(QThread):
    def __init__(self, port,  selfid, parent, pid, maxsize=1024):
        self.parent = parent
        self.pid = pid
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            self.sock.bind(('0.0.0.0', port))
        except OSError:
            # self.kill_port(port)
            self.sock.bind(("0.0.0.0", port))
        self.sock.listen(5)
        # self.sock.setblocking(False)
        self.thread_list = []
        if type(maxsize) == str:
            self.maxsize = int(maxsize)
        else:
            self.maxsize = maxsize
        self.selfid = selfid
        super(QThread, self).__init__()

    def run(self):
        try:
            try:
                csock, caddr = self.sock.accept()
                print("下载连接建立")
            except BlockingIOError:
                pass
            # print(caddr, "已连接")
            # t = Thread(target=self.handle_file, args=(csock, self.parent))
            # t.start()
            # self.parent.thread_list.append(t)
            # t.join()
            self.handle_file(csock, self.parent)
        finally:
            for x in self.thread_list:
                x.join()

    @staticmethod
    def kill_port(port):
        out = os.system('netstat -aon|findstr "4444"')
        os.kill(out, signal.SIGVTALRM)

    def handle_file(self, csock, parent):
        file_checked = False
        while True:
            data = csock.recv(self.maxsize)
            # 说明已经得到文件信息,创建好了文件
            if file_checked:
                if "f" not in locals():
                    f = open(addr+filename, "ab")

                if "zhanbao_data" in locals():
                    f.write(zhanbao_data[-1])
                    del zhanbao_data

                if not data or data == b"":
                    print("接收成功")
                    csock.close()

                    # self.parent.push_photo_into_chatwid(fileinf["sendid"], addr+filename, self.uid, self.uname)
                    parent.photolist.append([fileinf["sendid"], addr+filename])
                    # os.kill(self.pid, 26)
                    # parent.scan_photo_list()
                    self.quit()
                    return

                f.write(data)
            else:
                # 说明存在粘包
                if END_SEPARATE.encode(CHARSET) in data and not data.endswith(END_SEPARATE.encode(CHARSET)):
                    zhanbao_data = data.split(END_SEPARATE.encode(CHARSET))
                # 根据条件提取文件信息
                if data.startswith(OTHER_HEAD["FILE_INF_HEAD"].encode(CHARSET)) and not file_checked:
                    if "zhanbao_data" in locals():
                        fileinf = self.analyse_file(zhanbao_data[0].decode(CHARSET))
                    else:
                        fileinf = self.analyse_file(data.decode(CHARSET))
                    if not fileinf:
                        print("文件接收失败")
                        return
                    else:
                        # 确认文件信息
                        file_checked = True
                        # 生成地址
                        addr = self.get_addr() + self.selfid + "/"
                        filename = fileinf["filename"] + "_by_" + fileinf["sendid"] + fileinf["suffix"]
                        # 判断地址是否存在,不存在则创建
                        if not os.path.exists(addr):
                            os.makedirs(addr)
                        self.create_file(addr, filename)
                        continue

    def create_file(self, addr, filename):
        with open(addr + filename, "wb") as f:
            pass
        f.close()
        return

    # 已经确保传入的是完整类型的file信息
    # 文件信息格式头+自己的地址+文件名+发送方id+md5
    @staticmethod
    def analyse_file(data):
        datalist = data.split(FILE_SEPARATE)
        try:
            suffix = datalist[2].split(".")[-1]
            name = datalist[2].split(".")[:-1][0]
            addr = tuple(datalist[1].split(":"))
            datadic = {
                "selfaddr": addr,
                "filename": name,  # 保存的是不带后缀的文件名
                "suffix": "."+suffix,  # 保存文件的后缀名
                'sendid': datalist[3],
                "md5": datalist[-1]
            }
            return datadic
        except Exception as e:
            print("文件解包出现问题")
            return

    @staticmethod
    def get_addr():
        addr = os.getcwd()
        if addr.endswith("GUI"):
            addr = addr[:-3]
        if not addr.endswith("/"):
            addr += '/'
        addr += 'static/'
        return addr

    @staticmethod
    def get_host_ip():
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip


if __name__ == "__main__":
    x = recvSock(7895, "self")
    x.start()


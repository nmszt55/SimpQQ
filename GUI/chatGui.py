from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QScrollBar, QLabel
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor
from PyQt5.QtCore import QCoreApplication, Qt, QSize
from PyQt5.Qt import QTextEdit, QTextCursor
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket

from utils.UserMsgUnpick import msg_devide
from web.setting import *
from GUI.moveLabel import myLabel
from web.filesocket import Filesocket
import sys
import time


class ChatGui(QWidget):

    def __init__(self, *args, md5, selfid, msg, parent, selfname):
        if not args:
            return

        if len(args) != 1:
            self.type = "mul"
        else:
            self.type = "sin"
        self.parent = parent
        self.selfname = selfname
        self.msg = msg
        self.users = args
        self.selfid = selfid
        self.md5 = md5
        self.count_leav_msg = 0
        self.first = True
        self.sock = QTcpSocket()
        self.establish_connect()
        self.sock.readyRead.connect(self.ready_read)
        self.sock.connectToHost(SER_HOST, SER_PORT)

        super(ChatGui, self).__init__()
        self.initUI()

    def initUI(self):
        self.loadExitLabel()
        self.resize(500, 450)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.load_hidden_label()
        self.loadchatLabel()
        self.loadCHUIZHI()
        self.loadFuncBtns()
        self.loadsendmsgText()
        self.loadfuncbtn()
        self.loadSendBtn()
        # self.loadscrollbar()
        self.loadInf()

        self.show()

    def establish_connect(self):
        self.sock.connectToHost(SER_HOST, SER_PORT)
        if self.type == "sin":
            sstr = REQUEST_HEADS["BUILD_ESTABLISH_HEAD"] + SEPARATE + self.selfid + SEPARATE + self.users[0].get_id()\
                    + SEPARATE + self.md5
            self.sock.writeData(sstr.encode())

    def loadInf(self):
        self.inf_label = QLabel(self)
        self.inf_label.resize(120, 220)
        self.inf_label.move(370, 110)
        self.inf_label.setStyleSheet(testBorder)

        if self.type == "sin":  # 单人聊天
            headlabel = QLabel(self.inf_label)
            headlabel.resize(70, 70)
            headlabel.move(25, 25)
            headlabel.setStyleSheet(testBorder)
            if not self.users[0].get_head():
                headlabel.setPixmap(QPixmap(DEFAULT_HEAD))
            else:
                headlabel.setPixmap(QPixmap(self.users[0].get_head()))
            headlabel.setScaledContents(True)

            instrlabel = QLabel(self.inf_label)
            instrlabel.resize(100, 115)
            instrlabel.move(10, 100)
            if not self.users[0].get_intro():
                instrlabel.setText("这家伙很懒,什么都没有写")
            else:
                instrlabel.setText(self.users[0].get_intro())
            instrlabel.setWordWrap(True)
            instrlabel.setAlignment(Qt.AlignTop)

        if self.type == "mul":
            y = 10
            for user in self.users:
                llabel = QLabel(self.inf_label)
                llabel.setText(user.get_id()+" "+user.get_name())
                llabel.resize(100, 20)
                llabel.move(10, y)
                y += 25

    def loadExitLabel(self):
        exitbtn = QPushButton(self)
        exitbtn.setIcon(QIcon("../image/exit2.png"))
        exitbtn.adjustSize()
        exitbtn.move(472, -1)
        exitbtn.clicked.connect(self.close  )

    def load_hidden_label(self):
        hlabel = myLabel(self)
        hlabel.setText("群聊" if self.users == tuple else self.users[0].get_name())
        hlabel.setFixedWidth(472)
        hlabel.setFixedHeight(30)
        hlabel.move(0, 0)
        # hlabel.setHidden(True)
        self.m_flag = False

    def loadCHUIZHI(self):
        self.hbox = QHBoxLayout(self)

    def loadSendBtn(self):
        sendbtn = QPushButton(self)
        sendbtn.resize(120, 80)
        sendbtn.move(370, 365)
        sendbtn.setText('发送')
        sendbtn.setFont(QFont("Microsoft YaHei", 28))
        sendbtn.clicked.connect(self.doSend)

    def doSend(self):  # 处理发送消息函数
        msg = self.chatLabel.toPlainText()  # 获取内容
        self.addTextInEdit(username=self.selfname, msg=msg, type="send")
        if self.first:
            self.first = False
        self.chatLabel.setText("")
        # 打包消息 发送给服务器
        msg = self.msg_handler(msg)
        self.sock.writeData(msg.encode())
        if self.sock.state() != 3:
            msg = "[无连接]"+msg

    def msg_handler(self, msg):
        user_str = self.get_user_str()
        main_str = REQUEST_HEADS["SEND_MSG_HEAD"] + SEPARATE + MSG_START +\
                   msg + MSG_END + SEPARATE + self.selfid + SEPARATE + user_str + SEPARATE + self.md5
        return main_str

    def get_user_str(self):
        if self.type == "mul":
            ustr = ""
            for user in self.users:
                ustr += user.get_id() + USER_SEPARATE
        else:
            ustr = self.users[0].get_id()
        return ustr

    def ready_read(self):
        newmsg = self.sock.read(1024).decode()

        if newmsg.startswith(FAILED_HEADS["NOT_ONLINE_ERROR"]):
            self.addTextInEdit(username="错误消息", msg="对方未登录")
            return
        if newmsg.startswith(FAILED_HEADS["SEND_MESSAGE_FAILED"]):
            self.addTextInEdit(username="错误消息", msg="未知原因导致了发送失败")
            return
        if newmsg.startswith(FAILED_HEADS["BULID_ESTABLISH_FAILED"]):
            self.addTextInEdit(username="错误消息", msg="建立连接失败")
            return
        if newmsg.startswith(RESPONSE_HEADS["BULID_ESTABLISH_SUCCESS"]):
            print("建立聊天地址成功")
            return
        if newmsg.startswith(RECEIVE_MSG_HEAD["NEW_MSG_HEAD"]):
            self.analyse_msg(newmsg)

    def analyse_msg(self, data):
        datadic = msg_devide(data)
        if not datadic:
            print("因为未能识别包,一个信息被关闭了")
            return
        if datadic["md5"] != self.md5:
            print("一个不正确的md5发送过来")
            return
        if datadic["sid"] != self.selfid:
            print("一个非关联包被丢弃了")
            return

        self.addTextInEdit(self.users[0].get_name(), datadic["msg"], "recv")

    def addTextInEdit(self, username, msg, type="recv", sendtime=None):
        if not sendtime:  # 处理时时发送过来的消息
            date = list(time.localtime()[:6])
            timestr = ""
            for x in date:
                timestr += str(x)+"."
            if type == "recv":
                self.ChatLabel.setTextColor(QColor(32, 55, 96))
                self.ChatLabel.setAlignment(Qt.AlignLeft)
            if type == "send":
                self.ChatLabel.setTextColor(QColor(0, 55, 0))
                self.ChatLabel.setAlignment(Qt.AlignRight)
                if self.first == True:
                    # for x in range(self.count_leav_msg):
                    self.ChatLabel.insertPlainText("\r\n")

            self.ChatLabel.insertPlainText(username+"-"+timestr[:-1]+"\r\n")
            self.ChatLabel.insertPlainText(msg+"\r\n")
        else:  # 处理别人的留言
            self.ChatLabel.setTextColor(QColor(32, 55, 96))
            self.ChatLabel.setAlignment(Qt.AlignLeft)
            self.ChatLabel.insertPlainText(username + "-" + sendtime + "\r\n")
            self.ChatLabel.insertPlainText(msg + "\r\n")

    def loadchatLabel(self):
        self.ChatLabel = QTextEdit(self)
        # self.ChatLabel.setEnabled(False)
        self.ChatLabel.setReadOnly(True)
        self.ChatLabel.setFocusPolicy(Qt.NoFocus)
        self.ChatLabel.setFont(QFont("Microsoft YaHei", 10))
        self.ChatLabel.resize(340, 220)
        self.ChatLabel.move(20, 110)
        if self.msg:
            self.addTextInEdit(self.users[0].get_name(), self.msg, "recv")
        self.ChatLabel.textChanged.connect(self.loadscrollbar)

    def show_leaving_msg(self, msg, sendtime, username):
        self.count_leav_msg += 1
        self.addTextInEdit(username, msg, type="recv", sendtime=sendtime)

    def loadscrollbar(self):
        self.scr = QScrollBar(self)
        self.scr.resize(15, 220)
        self.scr.move(330, 110)
        self.ChatLabel.moveCursor(QTextCursor.End)

    def loadfuncbtn(self):  # 加载清屏按钮和发送图片按钮
        clearbtn = QPushButton(self)
        clearbtn.resize(30, 30)
        clearbtn.move(70, 332)
        clearbtn.setIcon(QIcon("../image/clear.png"))
        clearbtn.setIconSize(QSize(25, 25))
        clearbtn.clicked.connect(self.clear_text)
        clearbtn.show()

        photobtn = QPushButton(self)
        photobtn.resize(30, 30)
        photobtn.move(30, 332)
        photobtn.setIcon(QIcon("../image/photo.png"))
        photobtn.setIconSize(QSize(25, 25))
        photobtn.clicked.connect(self.send_photo_dialog)
        photobtn.show()

    # 清屏
    def clear_text(self):
        self.ChatLabel.clear()

    # 加载图片框体
    def send_photo_dialog(self):
        from PyQt5.QtWidgets import QFileDialog
        f = QFileDialog(self)

        fname = f.getOpenFileName(self, "send photo", "/home/tarena/", filter="Image File(*.jpg *.png)")
        # print(fname[0].split("/")[-1])
        if fname[0]:
            try:
                print("开始发送....")
                sender = Filesocket(self.selfid, self.users[0].get_id(), fname[0].split("/")[-1], MAX_FILESEND, self.md5)
                sender.start()
                with open(fname[0], "rb") as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        sender.send_file(data)
                    sender.close()
                    self.load_system_msg_in_charlabel("发送成功")
                    return True
            except IOError as e:
                print("加载文件出现错误,发送失败",e)
                return False

    def load_system_msg_in_charlabel(self, msg):
        self.ChatLabel.setTextColor(QColor(255, 0, 0))
        self.ChatLabel.setAlignment(Qt.AlignRight)
        self.ChatLabel.insertPlainText(msg+"\r\n")

    def loadFuncBtns(self):  # 加载顶部按钮
        self.funlist = []

        fun1 = QPushButton("下载", self)
        fun1.resize(40, 40)
        self.funlist.append(fun1)

        fun2 = QPushButton("邮件", self)
        fun2.resize(40, 40)
        self.funlist.append(fun2)

        i = 20
        for x in self.funlist:
            x.move(i, 50)
            i += 45

    def loadsendmsgText(self):
        self.chatLabel = QTextEdit(self)
        self.chatLabel.resize(340, 80)
        self.chatLabel.move(20, 365)
        # self.chatLabel.setAcceptRichText(True)

    def loadRight(self):
        if self.type == "mul":
            self.loadQunLiao()
        else:
            self.loadSingle()

    def closeEvent(self, eve):
        if self.type == "sin":
            main_str = REQUEST_HEADS["DELETE_CHAT_PORT_HEAD"] + SEPARATE + "<chataddr><{}><{}>".format(self.selfid,
                                                                                      self.users[0].get_id())
            self.sock.writeData(main_str.encode())
            self.parent.on_chat_close(self.users[0].get_id())

if __name__ == "__main__":
    appstart = QtWidgets.QApplication(sys.argv)
    sys.exit(appstart.exec_())
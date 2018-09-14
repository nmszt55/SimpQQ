from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QScrollBar, QLabel
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.Qt import QTextEdit, QTextCursor
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket

from web.setting import *
from GUI.moveLabel import myLabel
import sys


class ChatGui(QWidget):

    def __init__(self, *args, md5, selfid, msg):
        if not args:
            return

        if len(args) != 1:
            self.type = "mul"
        else:
            self.type = "sin"
        self.msg = msg
        self.users = args
        self.selfid = selfid
        self.md5 = md5
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
        exitbtn.clicked.connect(self.close)

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
        self.addTextInEdit(msg)
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
            self.addTextInEdit("对方未登录")
            return
        if newmsg.startswith(FAILED_HEADS["SEND_MESSAGE_FAILED"]):
            self.addTextInEdit("未知原因导致了发送失败")
            return
        if newmsg.startswith(FAILED_HEADS["BULID_ESTABLISH_FAILED"]):
            self.addTextInEdit("建立连接失败")
            return
        if newmsg.startswith(RESPONSE_HEADS["BULID_ESTABLISH_SUCCESS"]):
            print("建立聊天地址成功")
            return

    def analysis(self, msg):
        if type(self.users) != tuple:
            return self.users.get_name()
        else:
            return "abc"

    def addTextInEdit(self, msg):
        self.ChatLabel.insertPlainText(msg+"\r\n")

    def loadchatLabel(self):
        self.ChatLabel = QTextEdit(self)
        self.ChatLabel.setEnabled(False)
        self.ChatLabel.setFocusPolicy(Qt.NoFocus)
        self.ChatLabel.setFont(QFont("Microsoft YaHei",10))
        self.ChatLabel.setStyleSheet("color:#FF1493")
        self.ChatLabel.setAlignment(Qt.AlignRight)
        self.ChatLabel.resize(340, 220)
        self.ChatLabel.move(20, 110)
        if self.msg:
            self.ChatLabel.insertPlainText(self.msg)
        self.ChatLabel.textChanged.connect(self.loadscrollbar)



    def loadscrollbar(self):
        self.scr = QScrollBar(self)
        self.scr.resize(15,220)
        self.scr.move(330,110)
        self.ChatLabel.moveCursor(QTextCursor.End)

    def loadFuncBtns(self):
        self.funlist = []

        fun1 = QPushButton("下载",self)
        fun1.resize(40,40)
        self.funlist.append(fun1)

        fun2 = QPushButton("邮件",self)
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

    def loadRight(self):
        if self.type == "mul":
            self.loadQunLiao()
        else:
            self.loadSingle()


if __name__ == "__main__":
    appstart = QtWidgets.QApplication(sys.argv)
    x = ChatGui()
    sys.exit(appstart.exec_())
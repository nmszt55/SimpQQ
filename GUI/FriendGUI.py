#coding:utf-8
from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QDesktopWidget,QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QPalette,QBrush
from PyQt5.QtCore import QCoreApplication,Qt,QTimer,QDataStream
from PyQt5.Qt import QLineEdit
from PyQt5.QtNetwork import QTcpSocket

from functools import partial

from GUI.chatGui import ChatGui
from GUI.moveLabel import myLabel
from GUI.chatGui import ChatGui
from GUI.DoubleClickedLabel import MyQLabel
from GUI.AddFriend import AddFriend
from web.sqlFrame import SqlHelper
from web.setting import *
import sys

PORT = 8888
ADDR = '0.0.0.0'

class MyFrame(QMainWindow):
    def __init__(self, user):
        super(MyFrame, self).__init__()
        self.sqlhelper = SqlHelper()
        self.sock = QTcpSocket()
        self.user = user
        self.addfriend = AddFriend()
        self.x, self.y = 13, 10  # 记录朋友框高度
        self.__initUI()
        self.TryToConn()


    def __initUI(self):
        self.showOnlineMessage("自己")
        self.loadBackground()
        self.loadExitLabel()
        self.loadHideLabel()
        self.loadHideBtn()
        self.loadFriends()  # 判断好友数大于10出现滚动条
        self.loadMenu()  # 添加好友功能，加入群功能，创建群
        self.loadSearch()  # 搜索好友的框
        if self.user.get_head() is not None:
            self.loadSelf(Img=self.user.get_head(),Myname=self.user.get_name())  # 显示个人信息在顶上
        else:
            self.loadSelf(Myname=self.user.get_name())
        self.loadMain()

    def socketConnect(self):
        self.sock.connected.connect(self.SendRequest)
        self.sock.readyRead.connect(self.Readytoread)
        self.sock.disconnected().connect(self.DeleteLater)

    def SendRequest(self):
        self.hlabel.setText("Connecting...")

    def TryToConn(self):
        try:
            self.sock.connectToHost("127.0.0.1", 8081)
            if self.sock.state() == self.sock.ConnectingState:
                self.hlabel.setText("正在连接")
        except Exception as e:
            print(e)
            self.hlabel.setText("连接失败")

    def Readytoread(self):
        data = self.sock.readAll().decode()

        if data[:3] == "msg":
            """type,sendrid,recvid,data"""
            data = data.split(",")
            friends = data[2].split(" ")

        if data[:3] == 'ftp':
            pass

        if data[:3] == "mmg":  # 创建群聊：格式:mmg,sender,[user1id,user2id....]
            self.openMulChatWidget()  ################################################# 未实现

    def showOnlineMessage(self,username):
        # x = OnlineMsg(username)
        self.xlabel = QLabel()
        self.xlabel.setStyleSheet("font-size:25px;padding:10px;")
        self.xlabel.resize(150, 80)
        self.xlabel.setWindowFlags(Qt.FramelessWindowHint)
        self.xlabel.setText(username + "上线啦")

        pos = QDesktopWidget().availableGeometry().bottomRight()
        x = self.frameGeometry()
        x.moveCenter(pos)

        self.xlabel.move(x.bottomRight())
        self.xlabel.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.xlabel.close)
        self.timer.start(3000)

    def loadBackground(self):
        pat = QPalette()
        pat.setBrush(self.backgroundRole(),QBrush(QPixmap("../image/background1.jpg")))
        self.setPalette(pat)

    def loadMenu(self):
        addBtn = QPushButton(self)
        addBtn.resize(30,30)
        addBtn.setIcon(QIcon("../image/add.png"))
        addBtn.setStyleSheet("QPushButton{border-radius:20px}")
        addBtn.setStyleSheet("QPushButton:hover{background-color:red}")
        # addBtn.setStyleSheet('background-color:transparent')
        addBtn.clicked.connect(self.open_add_wit)

        multiBtn = QPushButton(self)
        multiBtn.setIcon(QIcon("../image/multiple.png"))
        multiBtn.resize(30,30)
        multiBtn.setStyleSheet("QPushButton{border-radius:20px}")
        multiBtn.setStyleSheet("QPushButton:hover{background-color:red}")
        # multiBtn.setStyleSheet('background-color:transparent')

        addBtn.move(20, 105)
        multiBtn.move(60, 105)

    def open_add_wit(self):
        self.addfriend.handle_click()

    def loadMain(self):
        self.resize(240,700)
        self.setWindowFlags(Qt.FramelessWindowHint)

        pos = QDesktopWidget().availableGeometry().topRight()
        x = self.frameGeometry()
        x.moveCenter(pos)

        self.move(x.topRight()*0.8)
        self.show()

    def loadHideLabel(self):
        self.hlabel = myLabel(self)
        self.hlabel.setText("             --对象")
        self.hlabel.setFixedWidth(212)
        self.hlabel.setFixedHeight(30)
        self.hlabel.move(0, 0)
        # self.hlabel.setHidden(True)
        self.m_flag = False

    def loadExitLabel(self):
        exitbtn = QPushButton(self)
        exitbtn.setIcon(QIcon("../image/exit2.png"))
        exitbtn.adjustSize()
        exitbtn.move(213,-1)
        exitbtn.clicked.connect(QCoreApplication.instance().quit)

    def loadHideBtn(self):
        Hidebtn = QPushButton(self)
        Hidebtn.setIcon(QIcon("../image/hide.png"))
        Hidebtn.adjustSize()
        Hidebtn.move(185,-1)
        Hidebtn.clicked.connect(self.showMinimized)

    def loadSelf(self, Img=default_head, Myname="ZZJ"):

        HeadLabel = QLabel(self)
        HeadLabel.resize(60,60)
        HeadLabel.move(25,40)
        Head = QPixmap(Img)
        # Head.scaled(40,40,aspectRatioMode=Qt.KeepAspectRatio)
        HeadLabel.setPixmap(Head)
        HeadLabel.setScaledContents(True)#设置图片自动缩放
        HeadLabel.setStyleSheet("border:2px solid #363636")

        name = QLabel(self)
        name.setText(Myname)
        name.resize(100,30)
        name.move(95,40)

    def loadSearch(self):
        SearchText = QLineEdit(self)
        SearchText.resize(200,30)
        SearchText.move(15,140)
        SearchText.setStyleSheet('background-color:transparent')
        SearchText.setPlaceholderText("在此输入寻找的用户名")

    def loadFriends(self):
        friends = self.sqlhelper.getFriends(self.user.get_id())

        Friends = QLabel(self)
        Friends.resize(200, 500)
        Friends.move(15, 185)
        Friends.setStyleSheet(testBorder)
        if not friends:
            Friends.setText("加载朋友失败")
            return
        for f in friends:
            Friend = MyQLabel(Friends)
            Friend.resize(170, 50)
            Friend.move(self.x, self.y)
            Friend.set_user(f, self)
            Friend.setStyleSheet(testBorder)

            head = f.get_head()
            if not head:
                head = default_head
            fHead = QLabel(Friend)
            fHead.resize(40, 40)
            fHead.setStyleSheet(testBorder)
            fHead.setPixmap(QPixmap(head))
            fHead.setScaledContents(True)
            fHead.move(5, 5)

            fname = QLabel(Friend)
            fname.setText(f.get_name())
            fname.move(55, 10)

            self.y += 55

    def openNewChat(self, user):
        ChatGui(user)




if __name__ == "__main__":
    appstart = QtWidgets.QApplication(sys.argv)
    x = MyFrame()
    sys.exit(appstart.exec_())
#coding:utf-8
from PyQt5.QtWidgets import QPushButton,QLabel,QDesktopWidget,QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QPalette,QBrush
from PyQt5.QtCore import QCoreApplication,Qt,QTimer
from PyQt5.Qt import QLineEdit
from PyQt5.QtNetwork import QTcpSocket

from functools import partial
from GUI.chatGui import ChatGui
from GUI.moveLabel import myLabel
from GUI.chatGui import ChatGui
from GUI.DoubleClickedLabel import MyQLabel
from GUI.AddFriend import AddFriend
from web.setting import *
from utils.UserMsgUnpick import friendunpick
import sys

PORT = 8888
ADDR = '0.0.0.0'

class MyFrame(QMainWindow):
    def __init__(self, user, MD5):
        super(MyFrame, self).__init__()
        self.sock = QTcpSocket()
        self.sock.connectToHost(SER_HOST, SER_PORT)

        self.user = user
        self.Key = MD5
        self.addfriend = AddFriend()
        self.__initUI()
        self.sock.connected.connect(self.SendRequest)
        self.sock.readyRead.connect(self.Readytoread)

    def resetFriendlocation(self):
        self.x, self.y = 13, 10

    def __initUI(self):
        self.showOnlineMessage("自己")
        self.loadBackground()
        self.loadExitLabel()
        self.loadHideLabel()
        self.loadHideBtn()
        self.resetFriendlocation()
          # 判断好友数大于10出现滚动条
        self.loadMenu()  # 添加好友功能，加入群功能，创建群
        self.loadSearch()  # 搜索好友的框
        self.loadFriends()

        if self.user.get_head() == None:
            self.loadSelf(Myname=self.user.get_name())  # 显示个人信息在顶上
        else:
            self.loadSelf(Img=self.user.get_head(), Myname=self.user.get_name())

    def SendRequest(self):
        self.hlabel.setText("Connecting...")

    def getfriends(self):
        requestdata = REQUEST_HEADS["GET_FRIENDS_HEAD"] + SEPARATE + self.user.get_id() + SEPARATE + self.Key
        self.sock.writeData(requestdata.encode())

    def Readytoread(self):
        print("接收消息")
        data = self.sock.read(MAX_DATA).decode()
        print("消息", data)
        if not data or data=="":
            return
        try:
            datalist = data.split(SEPARATE)

            if not self.md5_analyse(datalist[-1]):
                print("无MD5,不执行:",datalist[-1])
                return
            if datalist[0] not in RESPONSE_HEADS.values() and datalist[0] not in FAILED_HEADS.values():
                print("无效解析", datalist[0])
                return
            self.analyse_data(datalist)
        except Exception as e:
            print("分析过程出现问题",e)
            return

    def md5_analyse(self, psw):
        if self.Key != psw:
            return False
        else:
            return True

    def analyse_data(self, datalist):
        # 获取朋友的格式 <...>,friend_data
        if datalist[0] == RESPONSE_HEADS["GET_FRIENDS_SUCCESS"]:
            self.friends = friendunpick(datalist[1])
            self.loadFriends(self.friends)

        if datalist[0] == RESPONSE_HEADS["DELETE_FRIEND_SUCCESS"]:
            pass

        if datalist[0] == FAILED_HEADS["NO_FRIEND_HEAD"]:
            self.loadFriends(None)


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
        pat.setBrush(self.backgroundRole(), QBrush(QPixmap("../image/background1.jpg")))
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
        self.addfriend.handle_click(self.user.get_id(), self.sock, self.Key)

    def loadMain(self):
        self.resize(240, 700)
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
        exitbtn.move(213, -1)
        exitbtn.clicked.connect(QCoreApplication.instance().quit)

    def loadHideBtn(self):
        Hidebtn = QPushButton(self)
        Hidebtn.setIcon(QIcon("../image/hide.png"))
        Hidebtn.adjustSize()
        Hidebtn.move(185, -1)
        Hidebtn.clicked.connect(self.showMinimized)

    def loadSelf(self, Img=DEFAULT_HEAD, Myname="网络故障,请重新登录"):

        HeadLabel = QLabel(self)
        HeadLabel.resize(60, 60)
        HeadLabel.move(25, 40)
        Head = QPixmap(Img)
        # Head.scaled(40,40,aspectRatioMode=Qt.KeepAspectRatio)
        HeadLabel.setPixmap(Head)
        HeadLabel.setScaledContents(True)  # 设置图片自动缩放
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

    def loadFriends(self, friends=None):

        Friends = QLabel(self)
        Friends.resize(200, 500)
        Friends.move(15, 185)
        Friends.setStyleSheet(testBorder)

        if not friends:
            self.getfriends()
            return
        for f in friends:
            Friend = MyQLabel(Friends)
            Friend.resize(170, 50)
            Friend.move(self.x, self.y)
            Friend.set_user(f, self)
            Friend.setStyleSheet(testBorder)

            head = f.get_head()
            if not head:
                head = DEFAULT_HEAD
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
        self.loadMain()

    def openNewChat(self, user):
        ChatGui(user)




if __name__ == "__main__":
    appstart = QtWidgets.QApplication(sys.argv)
    x = MyFrame()
    sys.exit(appstart.exec_())
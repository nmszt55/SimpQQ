#coding:utf-8
import sys

from PyQt5 import QtWidgets,QtGui
from PyQt5.QtGui import QIcon,QMovie
from PyQt5.QtWidgets import QPushButton,QWidget,QMessageBox,QDesktopWidget,QMainWindow,QApplication
from PyQt5.QtWidgets import QAction,qApp,QTextEdit,QHBoxLayout,QVBoxLayout,QGridLayout,QLineEdit,QLabel
from PyQt5.QtCore import QCoreApplication,Qt,QUrl,QTimer
from utils.passwdSha1 import Sha1Translate
from PyQt5.QtNetwork import QTcpSocket,QAbstractSocket
from GUI.FriendGUI import MyFrame

from web.setting import *
from utils.UserMsgUnpick import unpick


class Mypyqt1(QWidget):

    def __init__(self):
        super().__init__()
        self.sock = QTcpSocket()
        # self.initUI()
        self.try_to_connect()
        self.timer = QTimer()
        self.sock.readyRead.connect(self.hand_msg)
        self.initUI()

    def try_to_connect(self):
        self.sock.connectToHost(SER_HOST, SER_PORT, )

    def hand_msg(self):
        response = self.sock.read(1024).decode()
        if response.startswith(RESPONSE_HEADS["LOGIN_SUCCESS"]):
            # 登记上次登录信息
            self.when_log_success(self.username)
            msg = response.split(SEPARATE)
            MD5 = msg[1]  # id秘钥
            user = unpick(msg[2])  # 用户的信息
            self.sock.close()
            self.close()
            MyFrame(user, MD5)

        if response.startswith(FAILED_HEADS["LOGIN_FAILED"]):
            self.loginfailed()
        else:
            self.loginfailed("出现了未知错误")

    def when_log_success(self, username):
        try:
            with open(LAST_LOGIN_ADDR, "w") as f:
                f.write(username)
        except:
            print("加载上次登录文件失败")

    def login(self):
        username = self.logintext.text()
        self.username = username
        password = Sha1Translate(self.password.text())

        if self.sock.state() != 3:
            self.loginfailed("请稍等,正在连接")
            return
        msg = REQUEST_HEADS["LOGIN_HEAD"] + SEPARATE + username + SEPARATE + password
        self.sock.writeData(msg.encode())

    def loadBackground(self):
        Blabel = QLabel(self)
        Blabel.resize(460,265)
        self.bgif = QMovie("../image/loging.gif")
        Blabel.setMovie(self.bgif)
        self.bgif.start()

    def loginfailed(self, strl="登录失败,请检查你的用户名和密码"):
        self.Iconing.resize(0, 0)
        self.LoginFail.setText(strl)
        self.LoginFail.setStyleSheet("color:red")

    def loadFont(self):
        logfont = QLabel(self)
        logfont.setText("用户名")
        logfont.setStyleSheet('''
        font-family: "Georgia", Tahoma, Sans-Serif;font-size: 20px;line-height: 18px;color: #888;
        ''')
        logfont.move(60,92)
        pswfont = QLabel(self)
        pswfont.setText("密    码")
        pswfont.setStyleSheet('''
        font-family: "Georgia", Tahoma, Sans-Serif;font-size: 20px;line-height: 18px;color: #888;
        ''')
        pswfont.move(60,126)

    def loadLastLogin(self):
        try:
            with open("../LastLogin.txt") as f:
                data = f.read()
                if not data or len(data)>10:
                    return ""
                return data
        except Exception:
            print("加载登录日志错误")
            return ""

    def LogingGUI(self):
        self.Iconing.resize(460,265)
        self.logingif = QMovie('../image/loging.gif')
        self.Iconing.setMovie(self.logingif)
        self.logingif.start()
        self.Iconing.show()


    def initUI(self):
#-----------------------------------------------------------------------------------------
        #初始化窗口
        # w = QtWidgets.QWidget()

# ----------------------------------------------------------------------------------------
        #退出按钮
        # exitbtn = QPushButton("退出",w)
        # exitbtn.move(20,20)
        # exitbtn.clicked.connect(QCoreApplication.instance().quit)

        #setGeometry()做了两件事：将窗口在屏幕上显示，并设置了它的尺寸。
        # setGeometry()方法的前两个参数定位了窗口的x轴和y轴位置。
        # 第三个参数是定义窗口的宽度，第四个参数是定义窗口的高度。
        # self.setGeometry(300,300,500,250)
# ----------------------------------------------------------------------------------------
#         self.ClassicFrame()
#         self.loadMenu()
#         self.loadStatusBar()
        self.loadBackground()
        self.loadButton()
        self.loadExitLabel()
        #设置不可改变大小
        self.setFixedSize(460,265)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()
        self.loadLineEdit()

        self.LoginFail = QLabel("", self)
        self.LoginFail.setFixedWidth(200)
        self.LoginFail.move(100,240)

        self.loadFont()

        self.Iconing = QLabel(self)
        self.Iconing.move(0,0)

        self.setWindowTitle("SimpQQ")
        self.setWindowIcon(QIcon(DEFAULT_ICON))

        self.show()

    #关闭窗口调用此函数
    # def closeEvent(self,event):
    #     reply = QMessageBox.question(self, 'Message',
    #                                  "Are you sure to quit?", QMessageBox.Yes |
    #                                  QMessageBox.No, QMessageBox.No)
    #
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    #移动至中心
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadMenu(self):
        #这个是菜单栏的封装
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        exitAction = QAction(QIcon('../image/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        # self.statusBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def loadStatusBar(self):
        '''这个是封装状态栏'''
        exitAction = QAction(QIcon('../image/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)


    def loadButton(self):
        # ----------------------------------------------------------------------------------------
        # 创建按钮
        loginbtn = QPushButton("登录", self)
        loginbtn.move(90, 200)
        loginbtn.resize(90, 30)
        loginbtn.clicked.connect(self.LogingGUI)
        loginbtn.clicked.connect(self.login)

        # 注册按钮
        resigbtn = QPushButton("注册", self)
        resigbtn.move(280, 200)
        resigbtn.resize(90, 30)
        resigbtn.clicked.connect(self.registerHtml)
        #
        # #装到盒子中
        # hbox = QHBoxLayout()
        # hbox.addStretch(1)
        # hbox.addWidget(loginbtn)
        # hbox.addWidget(resigbtn)
        #
        # vbox = QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addLayout(hbox)
        #
        # self.setLayout(vbox)

    def registerHtml(self):
        QtGui.QDesktopServices.openUrl(QUrl('http://localhost:8081/register.html'))


    #经典布局框架，剩余空间被text占用
    def ClassicFrame(self):
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

    def loadLineEdit(self):

        self.logintext = QLineEdit(self)
        self.logintext.resize(250,30)
        self.logintext.move(120,95)
        self.logintext.setText(self.loadLastLogin())
        self.logintext.setStyleSheet("""
        width:auto;
        margin-left:1px;
        float:left;
        font-family:Arial, Helvetica, sans-serif; 
        font-size:17px;
        color:#363636;
        """)

        self.password = QLineEdit(self)
        self.password.resize(250, 30)
        self.password.move(120,130)
        self.password.setEchoMode(self.password.Password)
        self.password.setStyleSheet("font-size:20px")

    def loadExitLabel(self):
        exitbtn = QPushButton(self)
        exitbtn.setIcon(QIcon("../image/exit2.png"))
        exitbtn.adjustSize()
        exitbtn.move(430,-1)
        exitbtn.clicked.connect(QCoreApplication.instance().quit)


if __name__=="__main__":
    appstart = QtWidgets.QApplication(sys.argv)
    x = Mypyqt1()
    sys.exit(appstart.exec_())
from PyQt5.QtWidgets import QWidget,QPushButton,QHBoxLayout,QScrollBar
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication,Qt
from PyQt5.Qt import QTextEdit,QTextCursor

from GUI.moveLabel import myLabel

import sys

class ChatGui(QWidget):
    def __init__(self,type="mul",**kwargs):
        super(ChatGui,self).__init__()
        self.__initUI()
        self.type = type
        self.userdict = kwargs#以ip为key，以用户实体为value的字典

    def __initUI(self):
        self.loadExitLabel()
        self.resize(500,450)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.load_hidden_label()
        self.loadchatLabel()
        self.loadCHUIZHI()
        self.loadFuncBtns()
        self.loadsendmsgText()
        self.loadSendBtn()
        # self.loadscrollbar()

        self.show()

    def loadSingle(self):
        self.loadTouxiang()
        self.loadInf()


    def loadExitLabel(self):
        exitbtn = QPushButton(self)
        exitbtn.setIcon(QIcon("../image/exit2.png"))
        exitbtn.adjustSize()
        exitbtn.move(472,-1)
        exitbtn.clicked.connect(self.close)

    def load_hidden_label(self):
        hlabel = myLabel(self)
        hlabel.setText("             --对象")
        hlabel.setFixedWidth(472)
        hlabel.setFixedHeight(30)
        hlabel.move(0,0)
        # hlabel.setHidden(True)
        self.m_flag = False

    def loadCHUIZHI(self):
        self.hbox = QHBoxLayout(self)

    def loadSendBtn(self):
        sendbtn = QPushButton(self)
        sendbtn.resize(120,80)
        sendbtn.move(370,365)
        sendbtn.setText('发送')
        sendbtn.setFont(QFont("Microsoft YaHei",28))
        sendbtn.clicked.connect(self.doSend)

    def doSend(self):#处理发送消息函数
        msg = self.chatLabel.toPlainText()#获取内容
        self.chatLabel.setText("")
        #判断消息发送成功，如果失败，在前面加上红字：[发送失败]
        self.addTextInEdit(msg)

    def addTextInEdit(self,msg):
        self.ChatLabel.insertPlainText(msg+"\r\n")

    def loadchatLabel(self):
        self.ChatLabel = QTextEdit(self)
        self.ChatLabel.setEnabled(False)
        self.ChatLabel.setFocusPolicy(Qt.NoFocus)
        self.ChatLabel.setFont(QFont("Microsoft YaHei",10))
        self.ChatLabel.setStyleSheet("color:#FF1493")
        self.ChatLabel.setAlignment(Qt.AlignRight)
        self.ChatLabel.resize(340,220)
        self.ChatLabel.move(20,110)
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
            x.move(i,50)
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
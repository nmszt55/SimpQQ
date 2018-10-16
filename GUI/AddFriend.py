from PyQt5.QtWidgets import QWidget,QDesktopWidget,QLineEdit,QPushButton,QLabel,QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import sys

from utils.UserMsgUnpick import addfriendunpick
from web.setting import *


class AddFriend(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        self.loadInput()
        self.loadSubmit()
        self.hidelabel()
        self.setStyleSheet("""
            QWidget{
                background-color: #4169E1;
            }
            QWidget#msgLabel{
                font-size: 40px;
                font-family: 'Microsoft Yahei';
            }
        """)
        # self.loadbackground()
        # self.loadHiddenLabel()
        # self.loadExitMenu()
        self.loadFriend()
        self.addbtn()

        self.loadSelf()
        self.closelabel()

    def md5_analyse(self, psw):
        if self.md5 != psw:
            return False
        else:
            return True

    def addbtn(self):
        self.add_friend_btn = QPushButton(self)
        self.add_friend_btn.resize(60, 30)
        self.add_friend_btn.setText("添加好友")
        self.add_friend_btn.clicked.connect(self.addfriend)
        self.add_friend_btn.move(145, 180)
        self.add_friend_btn.close()

    def hidelabel(self):
        self.headlabel = QLabel(self)
        self.namelabel = QLabel(self)
        self.idlabel = QLabel(self)
        self.headlabel.setStyleSheet(testBorder)
        self.namelabel.setStyleSheet(testBorder)
        self.idlabel.setStyleSheet(testBorder)

    def addfriend(self):
        opid = self.lineText.text()
        data = REQUEST_HEADS["ADD_FRIEND_HEAD"] + SEPARATE + opid + SEPARATE + self.uid + SEPARATE + self.md5
        self.sock.writeData(data.encode())

    def closelabel(self):
        self.nullLabel.show()
        self.add_friend_btn.close()
        self.idlabel.close()
        self.headlabel.close()
        self.namelabel.close()

    def loadSelf(self):
        self.setFixedSize(350, 300)
        self.center()
        self.setWindowTitle("添加好友")

    def handle_click(self, userid, sock , key):
        self.sock = sock
        self.uid = userid
        self.md5 = key
        self.show()

    def loadInput(self):
        self.lineText = QLineEdit(self)
        self.lineText.resize(250, 30)
        self.lineText.move(20, 250)
        self.lineText.setPlaceholderText("输入对方SQ号")

    def loadSubmit(self):
        submitBtn = QPushButton(self)
        submitBtn.resize(50, 30)
        submitBtn.setText("查找")
        submitBtn.move(274, 250)
        submitBtn.clicked.connect(self.search_friend)


    def search_friend(self):
        id_or_name = self.lineText.text()
        send_str = REQUEST_HEADS["GET_USER_HEAD"] + SEPARATE + id_or_name + SEPARATE + self.md5
        self.sock.writeData(send_str.encode())
        # if not user:
        #     self.nullLabel.setText("什么都没找到哦^-^")
        # else:
        #     self.friend = user
        #     self.loadFriend()


    def loadFriend(self):
        if not hasattr(self, "friend"):
            self.nullLabel = QLabel(self)
            self.nullLabel.setObjectName("msgLabel")
            self.nullLabel.resize(300, 200)
            self.nullLabel.setText("点击按钮查找>-<")
            self.nullLabel.move(25, 25)
        else:
            self.nullLabel.close()

            id = self.friend.get_id()
            id = "SQ号："+str(id)
            name = "对方昵称："+self.friend.get_name()
            head = self.friend.get_head()

            self.idlabel.setText(id)
            self.idlabel.move(145, 110)

            self.namelabel.setText(name)
            self.namelabel.move(130, 150)

            self.headlabel.resize(70, 70)
            if not head:
                self.headlabel.setPixmap(QPixmap(DEFAULT_HEAD))
            else:
                self.headlabel.setPixmap(QPixmap(head))
            self.headlabel.setScaledContents(True)
            self.headlabel.move(140, 30)

            self.idlabel.show()
            self.headlabel.show()
            self.namelabel.show()
            self.add_friend_btn.show()

    def closeEvent(self, event):
        event.accept()

    # 移动至中心
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def show_warn_msgbox(self, msg):
        reply = QMessageBox.information(self, "提示", msg,QMessageBox.Yes)

if __name__ == "__main__":
    appstart = QtWidgets.QApplication(sys.argv)
    addfriend = AddFriend()
    addfriend.show_warn_msgbox()
    sys.exit(appstart.exec_())
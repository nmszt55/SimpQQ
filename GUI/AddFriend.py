from PyQt5.QtWidgets import QWidget,QDesktopWidget,QLineEdit,QPushButton,QLabel
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import sys

from web.sqlFrame import sqlhelper
from web.setting import *


class AddFriend(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        self.loadInput()
        self.loadSubmit()
        self.hidelabel()
        # self.loadbackground()
        # self.loadHiddenLabel()
        # self.loadExitMenu()
        self.loadFriend()
        self.loadSelf()
        self.closelabel()


    def hidelabel(self):
        self.headlabel = QLabel(self)
        self.namelabel = QLabel(self)
        self.idlabel = QLabel(self)
        self.headlabel.setStyleSheet(testBorder)
        self.namelabel.setStyleSheet(testBorder)
        self.idlabel.setStyleSheet(testBorder)

    def closelabel(self):
        self.idlabel.close()
        self.headlabel.close()
        self.namelabel.close()

    def loadSelf(self):
        self.setFixedSize(350, 300)
        self.center()
        self.setWindowTitle("添加好友")

    def handle_click(self):
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
        user = sqlhelper.fetch_an_friend(id_or_name)
        if not user:
            self.nullLabel.setText("什么都没找到哦^-^")
        else:
            self.friend = user
            self.loadFriend()


    def loadFriend(self):
        if not hasattr(self, "friend"):
            self.nullLabel = QLabel(self)
            self.nullLabel.resize(300, 250)
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
            self.headlabel.setPixmap(QPixmap(head))
            self.headlabel.move(140, 30)

            self.idlabel.show()
            self.headlabel.show()
            self.namelabel.show()

    def closeEvent(self, event):
        event.accept()

    # 移动至中心
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    appstart = QtWidgets.QApplication(sys.argv)
    addfriend = AddFriend()
    sys.exit(appstart.exec_())
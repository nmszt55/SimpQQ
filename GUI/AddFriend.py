from PyQt5.QtWidgets import QWidget,QDesktopWidget,QLineEdit,QPushButton,QLabel
from PyQt5 import QtWidgets
import sys


class AddFriend(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        self.loadInput()
        self.loadSubmit()
        # self.loadbackground()
        # self.loadHiddenLabel()
        # self.loadExitMenu()
        self.loadFriend()
        self.loadSelf()

    def loadSelf(self):
        self.setFixedSize(350,300)
        self.center()
        self.setWindowTitle("添加好友")
        self.show()

    def loadInput(self):
        lineText = QLineEdit(self)
        lineText.resize(250, 30)
        lineText.move(20,250)
        lineText.setPlaceholderText("输入对方SQ号")

    def loadSubmit(self):
        submitBtn = QPushButton(self)
        submitBtn.resize(50,30)
        submitBtn.setText("查找")
        submitBtn.move(274,250)

    def loadFriend(self):
        if not hasattr(self,"friend"):
            nullLabel = QLabel(self)
            nullLabel.resize(300,250)
            nullLabel.setText("查找用户界面")
            nullLabel.move(25,25)
        else:
            friendlabel = QLabel(self)
            friendlabel.resize(300,250)
            name = self.friend.get_name()
            head = self.friend.get_head()
            instr = self.friend.get_intro()
            .....



    #移动至中心
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    appstart = QtWidgets.QApplication(sys.argv)
    x = AddFriend()
    sys.exit(appstart.exec_())
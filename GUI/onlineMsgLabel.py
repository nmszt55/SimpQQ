from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QDesktopWidget
from PyQt5.QtGui import QIcon,QPixmap,QPalette,QBrush
from PyQt5.QtCore import QCoreApplication,Qt,QTimer
from PyQt5 import QtWidgets
import sys


class OnlineMsg(QLabel):
    def __init__(self,username="zzj"):
        super(OnlineMsg,self).__init__()
        self.username = username
        self.showOnlineMessage()

    def showOnlineMessage(self):
        self.setStyleSheet("font-size:25px;padding:10px;")
        self.resize(150,80)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setText(self.username+"上线啦")

        pos = QDesktopWidget().availableGeometry().bottomRight()
        x = self.frameGeometry()
        x.moveCenter(pos)

        self.move(x.bottomRight())
        self.show()



if __name__ == "__main__":
    appstart = QtWidgets.QApplication(sys.argv)
    x = OnlineMsg()
    sys.exit(appstart.exec_())
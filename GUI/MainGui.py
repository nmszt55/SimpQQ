#coding:utf-8
from PyQt5.QtWidgets import QWidget

class MainGui(QWidget):
    def __init__(self):
        super().__init__()

        self.user = getUser()
        self.friend = getFriendsByUser(self.user)
        self.__initUI()

    def __initUI(self):
        pass
from PyQt5.QtWidgets import QLabel
from GUI.chatGui import ChatGui
from GUI.FriendGUI import *

class MyQLabel(QLabel):

    def set_user(self, user, parent):
        self.user = user
        self.parent = parent

    def mouseDoubleClickEvent(self, e):
        self.parent.openNewChat(self.user)

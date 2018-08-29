from PyQt5.QtWidgets import QLabel
from GUI.chatGui import ChatGui

class MyQLabel(QLabel):
    def setUser(self,User):
        self.user = User
    def mouseDoubleClickEvent(self, e):
        ChatGui()
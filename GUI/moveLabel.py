
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

class myLabel(QLabel):
    def __init__(self,parent = None):
        super(myLabel,self).__init__(parent)
        self.m_flag=False
        self.parent = parent
#--------------------以下方法为判断鼠标并拖动屏幕----------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.parent.m_Position = event.globalPos() - self.parent.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.parent.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.parent.move(QMouseEvent.globalPos()-self.parent.m_Position)#更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.parent.setCursor(QCursor(Qt.ArrowCursor))

#-------------------------------------------------------------------
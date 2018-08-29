from PyQt5.QtCore import QThread,pyqtSignal
import time


class Mythread(QThread):
    sec_changed_signal = pyqtSignal(int)  # 信号类型：int

    def __init__(self, sec=1000, parent=None):
        super().__init__(parent)
        self.sec = sec  # 默认1000秒

    def run(self):
        time.sleep(5)
        self.sec_changed_signal.emit(i)  # 发射信号

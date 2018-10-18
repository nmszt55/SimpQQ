from PyQt5.QtCore import QThread, QTimer

import time


class Mythread(QThread):
    def __init__(self, list, parent):
        self.list = list
        super(QThread, self).__init__(parent)

    def run(self):
        while True:
            if self.list:
                if len(self.list) > 0:
                    for x in self.list:
                        self.list.append(x)
                        return
            time.sleep(1)


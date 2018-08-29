from PyQt5.QtWidgets import QScrollArea


class QS(QScrollArea):

    def __init__(self,*args):
        super(QS, self).__init__(*args)
    # def wheelEvent(self, e):
    #     pass # 这里是取消了原有的滚动条滚动时的操作 以免出现滚动了而我们自己的滚动条按钮没有变化
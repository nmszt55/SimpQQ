#coding:utf-8
from PyQt5.QtWidgets import QPushButton, QLabel, QDesktopWidget, QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush
from PyQt5.QtCore import QCoreApplication, Qt, QTimer
from PyQt5.Qt import QLineEdit
from PyQt5.QtNetwork import QTcpSocket


# from functools import partial
# from GUI.chatGui import ChatGui
from GUI.moveLabel import myLabel
from GUI.chatGui import ChatGui
from GUI.DoubleClickedLabel import MyQLabel
from GUI.AddFriend import AddFriend
from web.setting import *
from utils.UserMsgUnpick import *
from domain.user import user
from web.filerecvsock import recvSock
import sys
import time
import os
import signal
from threading import Thread


class MyFrame(QMainWindow):
    def __init__(self, user, MD5):
        signal.signal(signal.SIGUSR1, self.scan_photo_list)
        super(MyFrame, self).__init__()
        self.sock = QTcpSocket()
        self.sock.connectToHost(SER_HOST, SER_PORT)
        self.sock.connected.connect(self.SendRequest)
        self.sock.readyRead.connect(self.Readytoread)
        self.setWindowIcon(QIcon(DEFAULT_ICON))
        self.chatdic = {}
        self.friends_online = {}  # 用来存储用户的显示上线的label
        self.photolist = []
        self.user = user
        self.Key = MD5
        self.count = 1

        if not hasattr(self, "friends"):
            print("发送好友请求")
            self.getfriends()

        self.addfriend = AddFriend()
        self.__initUI()
        self.show()

    def resetFriendlocation(self):
        self.x, self.y = 13, 10

    def __initUI(self):
        self.setStyleSheet("""
        QMainWindow{
            border-radius: 10%;
            background-color: #4169E1;
            color: #696969;
        }
        MyQLabel:hover{
            background-color: #D3D3D3;
        }
        MyQLabel{
            border:1px solid #808080;
            border-radius: 3.5%;
        }
        QLabel#Friends{
            background-color: #6495ED;
            border: 1px solid #5F9EA0;
        }
        """)

        self.setWindowOpacity(0.8)
        self.friends_init()
        self.onlinemsg_init()
        # self.showOnlineMessage(self.user.get_name()+"上线啦")
        self.loadBackground()
        self.loadExitLabel()
        self.loadHideLabel()
        self.loadHideBtn()
        self.resetFriendlocation()
        # 判断好友数大于10出现滚动条
        self.loadMenu()  # 添加好友功能，加入群功能，创建群
        self.loadSearch()  # 搜索好友的框
        if self.user.get_head() == None:
            self.loadSelf(Myname=self.user.get_name())  # 显示个人信息在顶上
        else:
            self.loadSelf(Img=self.user.get_head(), Myname=self.user.get_name())

    def SendRequest(self):
        self.hlabel.setText("Connecting...")

    def getfriends(self):
        requestdata = REQUEST_HEADS["GET_FRIENDS_HEAD"] + SEPARATE + self.user.get_id() + SEPARATE + self.Key
        self.sock.writeData(requestdata.encode())
        # self.sock.flush()

    def correct_port(self):
        str1 = REQUEST_HEADS["CORRECT_ADDR_HEAD"] + SEPARATE + self.user.get_id() + SEPARATE + self.Key
        self.sock.writeData(str1.encode())

    def friends_search(self):
        if not hasattr(self, "friends"):
            return
        text = self.SearchText.text()
        if not text:
            self.reload_friends(self.friends)
            return
        fs = []
        for x in self.friends:
            if text in x.get_name() or text in str(x.get_id()):
                fs.append(x)
        if len(fs) == 0:
            self.reload_friends(None)
        else:
            self.reload_friends(fs)

    def Readytoread(self, adata=None):
        if not adata:
            data = self.sock.read(MAX_DATA).decode(CHARSET)
            if is_zhanbao(data):  # 出现粘包进行分离
                commands = zhanbao_devide(data)
                for x in commands:
                    if not x:
                        continue
                    self.Readytoread(adata=x)
                return
            else:
                pass
        else:
            data = adata

        if not data or data == "":
            return
        try:
            if data.startswith(OTHER_HEAD["NEED_TO_RECV_FILE_HEAD"]):
                print("接收文件启动1")
                dic = getfileinf(data)
                if not dic:
                    print("提取文件信息失败")
                    return
                else:
                    if dic["maxdata"]:
                        sock = recvSock(FILE_RECV_PORT, self.user.get_id(), dic['maxdata'])
                    else:
                        sock = recvSock(FILE_RECV_PORT, self.user.get_id())
                    t = Thread(target=sock.start, args=(self, os.getpid()))
                    t.setDaemon(True)
                    t.start()
                    stri = RESPONSE_HEADS["CREATE_RECV_FILE_CONN"] + FILE_SEPARATE + self.user.get_id() + FILE_SEPARATE\
                        + sock.get_host_ip()+":"+str(FILE_RECV_PORT) + FILE_SEPARATE + self.Key
                    self.sock.writeData(stri.encode(CHARSET))

            datalist = data.split(SEPARATE)
            if datalist[0] == FAILED_HEADS["ILLEGAL_HEAD"]:
                print("非法格式,请检查服务器源代码")
                return
            if not self.md5_analyse(data):
                print("无MD5,不执行:", data)
                return
            if datalist[0] == RECEIVE_MSG_HEAD["NEW_MSG_HEAD"]:
                self.analyse_msg(data)
                return
            if datalist[0] == RECEIVE_MSG_HEAD['LEAVE_MSG_HEAD']:
                self.analyse_leaving_msg(data)
                return
            if datalist[0] not in RESPONSE_HEADS.values() and datalist[0] not in FAILED_HEADS.values():
                if datalist[0].split(FILE_SEPARATE)[0] not in OTHER_HEAD.values():
                    print("无效解析", datalist[0])
                    return
            self.analyse_data(datalist)
        except Exception as e:
            print("分析过程出现问题", e)
            raise e
            return

    def scan_photo_list(self, a, b):
        print("开始扫描队列", self.photolist)
        if len(self.photolist) > 0:
            for x in self.photolist:
                self.push_photo_into_chatwid(x[0], x[1])
                self.photolist.remove(x)

    def push_photo_into_chatwid(self, sendid, photomsg):
        try:
            if self.chatdic[sendid]:
                pass
        except KeyError:
            for x in self.friends:
                if x.get_id() == sendid:
                    usr = x
            self.chatdic[sendid] = ChatGui(usr, md5=self.Key, selfid=self.user.get_id(), msg=None,
                                                  parent=self, selfname=self.user.get_name())
        finally:
            self.chatdic[sendid].ChatLabel.insertHtml("<img src={} alt={} width='150' height='100'><br>".
                                                      format(photomsg, "can found image"))
            self.chatdic[sendid].show()
            stri = REQUEST_HEADS["CLOSE_FILE_ADDR_PORT"] + SEPARATE + self.user.get_id()
            self.sock.writeData(stri.encode(CHARSET))

    def md5_analyse(self, data):
        if data.endswith(END_SEPARATE):
            if not data[:-len(END_SEPARATE)].endswith(self.Key):
                return False
            else:
                return True
        else:
            if data.endswith(self.Key):
                return True
            else:
                return False

    def analyse_leaving_msg(self, data):
        msgdic = leaving_msg_unpuck(data)
        if not msgdic:
            print("分析无结果")
            return
        if msgdic["sid"] != self.user.get_id():
            print("分析结果不正却", msgdic["sid"])
            return
        if msgdic["md5"] != self.Key:
            if msgdic["md5"].endswith(END_SEPARATE):
                if msgdic["md5"][:-len(END_SEPARATE)] != self.Key:
                    print("一个不正确的md5发送过来", msgdic["md5"])
                    return

        for f in self.friends:
            if msgdic["fromid"] == f.get_id():
                if f.get_id() not in self.chatdic:
                    self.openNewChat(f, msgdic["msg"], datetime=msgdic["sendtime"])
                    break
                else:
                    self.chatdic[f.get_id()].show_leaving_msg(msgdic["msg"], msgdic["sendtime"], f.get_name())

    def analyse_data(self, datalist):
        # 获取朋友的格式 <...>,friend_data
        if datalist[0] == RESPONSE_HEADS["GET_FRIENDS_SUCCESS"]:
            self.friends, onlinelist = friendunpick(datalist[1])
            self.loadFriends(self.friends)
            # self.reload_friends(self.friends)
            self.update_online(onlinelist)

        if datalist[0] == RESPONSE_HEADS["DELETE_FRIEND_SUCCESS"]:
            pass

        if datalist[0] == FAILED_HEADS["NO_FRIEND_HEAD"]:
            self.loadFriends(None)

        if datalist[0] == FAILED_HEADS["CORRECT_PORT_FAILED"]:
            print("矫正端口失败,可能无法接收消息")

        if datalist[0] == RESPONSE_HEADS["CORRECT_PORT_SUCCESS"]:
            print("端口矫正成功")

        if datalist[0] == RESPONSE_HEADS["GET_USR_SUCCESS"]:
            userdata = datalist[1]
            added_user = addfriendunpick(userdata)
            if not added_user:
                print("代码出错啦")
                return
            self.addfriend.friend = added_user
            self.addfriend.loadFriend()

        if datalist[0] == FAILED_HEADS["NO_USER_HEAD"]:
            self.addfriend.closelabel()
            self.addfriend.nullLabel.setText("未找到用户")

        if datalist[0] == FAILED_HEADS["ADD_FRIEND_FAILED"]:
            self.addfriend.closelabel()
            self.addfriend.nullLabel.setText("因为服务器原因添加好友失败")

        if datalist[0] == FAILED_HEADS["FRIEND_ALREADY_EXISTS"]:
            self.addfriend.closelabel()
            self.addfriend.nullLabel.setText("你们已经是好友啦")

        if datalist[0] == FAILED_HEADS["CANNOT_ADD_SELF_ERROR"]:
            self.addfriend.closelabel()
            self.addfriend.nullLabel.setText("不能添加自己为好友哦~~")

        if datalist[0] == RESPONSE_HEADS["ADD_FRIEND_SUCCESS"]:
            self.count += 1
            self.showOnlineMessage("添加好友成功")
            usr = user(*datalist[1].split(ATTR_SERARATE)[:2])
            try:
                usr.set_head(datalist[1].split(ATTR_SERARATE)[2])
            except:
                usr.set_head(DEFAULT_HEAD)
            if not hasattr(self, "friends"):
                self.friends = []
            self.friends.append(usr)
            self.reload_friends(self.friends)

        # 处理上线消息
        if datalist[0] == RESPONSE_HEADS["ONLINE_HEAD"]:
            uid = datalist[2]
            if uid in self.friends_online:
                self.friends_online[uid].close()
                self.friends_online[uid].setText("上线")
                self.friends_online[uid].show()
                if hasattr(self, "friends"):
                    for x in self.friends:
                        if x.get_id() == uid:
                            self.showOnlineMessage(x.get_name() + "上线")

        # 接收下线消息,处理相关结果
        if datalist[0] == RESPONSE_HEADS["UNDERLINE_HEAD"]:
            uid = datalist[2]
            if uid not in self.friends_online:
                return
            self.friends_online[uid].close()
            self.friends_online[uid].setText("下线")
            self.friends_online[uid].show()
            if hasattr(self, "friends"):
                for x in self.friends:
                    if x.get_id() == uid:
                        self.showOnlineMessage(x.get_name() + "已经下线")

    def update_online(self, online):
        for x in online:
            if x[1]:
                self.friends_online[x[0]].setText("上线")
            else:
                self.friends_online[x[0]].setText("下线")

    def reload_friends(self, fris):
        # self.Friends.clear()
        # self.Friends.close()
        self.resetFriendlocation()
        self.loadFriends(fris)
        # self.Friends.show()

    def analyse_msg(self, data):
        datadic = msg_devide(data)
        if not datadic:
            print("因为未能识别包,一个信息被关闭了")
            return
        if datadic["md5"] != self.Key+END_SEPARATE and datadic["md5"] != self.Key:
            print("一个不正确的md5发送过来")
            return
        if datadic["sid"] != self.user.get_id():
            print("一个非关联包被丢弃了")
            return
        for f in self.friends:
            if datadic["oid"] == f.get_id():
                if f.get_id() not in self.chatdic:
                    self.openNewChat(f, datadic["msg"])
                    break
                else:
                    self.chatdic[f.get_id()].addTextInEdit(datadic["msg"])
                    break

    def onlinemsg_init(self):
        self.xlabel = QLabel()
        self.xlabel.setStyleSheet("font-size:25px;padding:10px;")
        self.xlabel.resize(150, 80)
        self.xlabel.setWindowFlags(Qt.FramelessWindowHint)
        self.timer = QTimer()

    def showOnlineMessage(self, stri):
        # x = OnlineMsg(username)
        if stri:
            self.xlabel.setText(stri)
        pos = QDesktopWidget().availableGeometry().bottomRight()
        x = self.frameGeometry()
        x.moveCenter(pos)

        self.xlabel.move(x.bottomRight())
        self.xlabel.show()

        self.timer.timeout.connect(self.xlabel.close)
        self.xlabel.show()
        self.timer.start(3000)

    def loadBackground(self):
        pat = QPalette()
        # pat.setBrush(self.backgroundRole(), QBrush(QPixmap("../image/background1.jpg")))
        self.setPalette(pat)

    def loadMenu(self):
        addBtn = QPushButton(self)
        addBtn.resize(30, 30)
        addBtn.setIcon(QIcon("../image/add.png"))
        addBtn.setStyleSheet("QPushButton{border-radius:20px}")
        addBtn.setStyleSheet("QPushButton:hover{background-color:red}")
        # addBtn.setStyleSheet('background-color:transparent')
        addBtn.clicked.connect(self.open_add_wit)

        multiBtn = QPushButton(self)
        multiBtn.setIcon(QIcon("../image/multiple.png"))
        multiBtn.resize(30,30)
        multiBtn.setStyleSheet("QPushButton{border-radius:20px}")
        multiBtn.setStyleSheet("QPushButton:hover{background-color:red}")
        # multiBtn.setStyleSheet('background-color:transparent')

        addBtn.move(20, 105)
        multiBtn.move(60, 105)

    def open_add_wit(self):
        self.addfriend.handle_click(self.user.get_id(), self.sock, self.Key)

    def loadMain(self):
        self.resize(240, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)

        pos = QDesktopWidget().availableGeometry().topRight()
        x = self.frameGeometry()
        x.moveCenter(pos)

        self.move(x.topRight()*0.8)
        self.show()

    def loadHideLabel(self):
        self.hlabel = myLabel(self)
        self.hlabel.setText("             "+self.user.get_name())
        self.hlabel.setFixedWidth(212)
        self.hlabel.setFixedHeight(30)
        self.hlabel.move(0, 0)
        # self.hlabel.setHidden(True)
        self.m_flag = False

    def loadExitLabel(self):
        exitbtn = QPushButton(self)
        exitbtn.setIcon(QIcon("../image/exit2.png"))
        exitbtn.adjustSize()
        exitbtn.move(213, -1)
        exitbtn.clicked.connect(QCoreApplication.instance().quit)

    def loadHideBtn(self):
        Hidebtn = QPushButton(self)
        Hidebtn.setIcon(QIcon("../image/hide.png"))
        Hidebtn.adjustSize()
        Hidebtn.move(185, -1)
        Hidebtn.clicked.connect(self.showMinimized)

    def loadSelf(self, Img=DEFAULT_HEAD, Myname="网络故障,请重新登录"):
        HeadLabel = QLabel(self)
        HeadLabel.resize(60, 60)
        HeadLabel.move(25, 40)
        Head = QPixmap(Img)
        # Head.scaled(40,40,aspectRatioMode=Qt.KeepAspectRatio)
        HeadLabel.setPixmap(Head)
        HeadLabel.setScaledContents(True)  # 设置图片自动缩放
        HeadLabel.setStyleSheet("border:2px solid #363636")

        name = QLabel(self)
        name.setText(Myname)
        name.resize(100, 30)
        name.move(95, 40)

    def loadSearch(self):
        self.SearchText = QLineEdit(self)
        self.SearchText.resize(200, 30)
        self.SearchText.move(15, 140)
        self.SearchText.setStyleSheet('background-color:transparent')
        self.SearchText.setPlaceholderText("在此输入寻找的用户名")
        self.SearchText.textChanged.connect(self.friends_search)

    def friends_init(self):
        self.Friends = QLabel(self)
        self.Friends.resize(200, 500)
        self.Friends.move(15, 185)
        self.Friends.setObjectName("Friends")
        # self.Friends.setStyleSheet(testBorder)

    def loadFriends(self, friends=None):
        if not friends:
            self.Friends.close()
            # self.Friends.setText("查找不到好友")
            return
        if friends:
            del self.Friends
            self.friends_init()
            for f in friends:
                Friend = MyQLabel(self.Friends)
                Friend.resize(170, 50)
                Friend.move(self.x, self.y)
                Friend.set_user(f, self)
                # Friend.setStyleSheet(testBorder)

                head = f.get_head()
                if not head:
                    head = DEFAULT_HEAD
                fHead = QLabel(Friend)
                fHead.resize(40, 40)
                # fHead.setStyleSheet(testBorder)
                fHead.setPixmap(QPixmap(head))
                fHead.setScaledContents(True)
                fHead.move(5, 5)

                fname = QLabel(Friend)
                fname.setText(f.get_name())
                fname.move(55, 5)

                fonline = QLabel(Friend)
                fonline.move(55, 25)
                fonline.resize(40, 20)
                self.friends_online[f.get_id()] = fonline

                self.y += 55
            self.Friends.show()
        if self.count == 1:  # 表示第一次加载
            QApplication.processEvents()
            self.loadMain()
            self.correct_port()
            self.count += 1

    def openNewChat(self, user, msg=None, datetime=None):
        try:
            if self.chatdic[user.get_id()]:
                self.chatdic[user.get_id()].show()
        except KeyError:
            if not datetime:
                if msg:
                    self.chatdic[user.get_id()] = ChatGui(user, md5=self.Key, selfid=self.user.get_id(), msg=msg, parent=self
                                                      , selfname=self.user.get_name())
                else:
                    self.chatdic[user.get_id()] = ChatGui(user, md5=self.Key, selfid=self.user.get_id(), msg=None,
                                                          parent=self, selfname=self.user.get_name())
            else:
                print("开始执行打开窗口")
                self.chatdic[user.get_id()] = ChatGui(user, md5=self.Key, selfid=self.user.get_id(), msg=None, parent=self
                                                      , selfname=self.user.get_name())
                self.chatdic[user.get_id()].show_leaving_msg(msg, datetime, user.get_name())

    def on_chat_close(self, uid):
        print("检测状态:", end="")
        print(self.chatdic.pop(uid, None))


if __name__ == "__main__":
    appstart = QtWidgets.QApplication(sys.argv)
    x = MyFrame()
    sys.exit(appstart.exec_())
from web.setting import *
import pymysql
from utils.passwdSha1 import Sha1Translate
from domain.user import user

class SqlHelper(object):
    def __init__(self):
        try:
            self.__conn = pymysql.connect(host=host, port=port, db=DB, user=USERNAME, passwd=PASSWD, charset="utf8")
        except Exception as e:
            print("连接被拒绝")
            return
        self.cr = self.__conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self,"cr"):
            self.cr.close()
        self.__conn.close()
        print("关闭连接")

    def query(self, sql, param=[]):
        try:
            self.cr.execute(sql, param)
            data = self.cr.fetchall()
            return data
        except Exception as e:
            print(e)
            print("出错")
            return

    def fetch_an_friend(self,IdOrName):
        try:
            try:
                IdOrName = int(IdOrName)
            except:
                sql = "select id,nickname,head from user WHERE nickname=%s"
            else:
                sql = "select id,nickname,head from user WHERE id=%s"

            param = (IdOrName)
            self.cr.execute(sql, param)
            usr = self.cr.fetchone()

            if not usr:
                return None

            ur = user(usr[0], usr[1])
            if not usr[2]:
                ur.set_head(default_head)
                return ur

            ur.set_head(usr[2])
            return ur
        except Exception as e:
            print("查找好友出错")
            print(e)
            return None

    def addfriend(self, selfid, friendid):
        try:
            sql = 'insert into friend(uid1,uid2) values(%s,%s)'
            param = (selfid, friendid)
            self.cr.execute(sql, param)
            self.__conn.commit()
            return True
        except Exception as e:
            self.__conn.rollback()
            print(e)
            print("添加好友出错")
            return False

    def register(self, name, password, nickname):
        try:
            sql = "insert into user(name,password,nickname) values(%s,%s,%s)"
            param = (name, Sha1Translate(password), nickname)
            self.cr.execute(sql, param)
            self.__conn.commit()
            return True
        except Exception as e:
            self.__conn.rollback()
            return False

    def getFriends(self, selfid):  # 查找好友
        try:
            sql = friendsql
            param = (selfid,selfid,selfid)
            self.cr.execute(sql,param)
            data = self.cr.fetchall()
            flist = []
            for x in data:
                u = user(x[0], x[1])
                if not x[2]:
                    u.set_head(x[2])
                flist.append(u)
            return flist
        except Exception as e:
            print(e)
            return None

sqlhelper = SqlHelper()

if __name__ == "__main__":
    with SqlHelper() as sh:
        data = sh.getFriends(2)
        for x in data:
            print(x)

        # if sh.addfriend(2,7):
        #     print("添加好友成功")

        # while True:
        #     un = input("输入用户名")
        #     pw = input("输入密码")
        #     nn = input("输入昵称")
        #     if sh.register(un, pw, nn):
        #         print("注册成功")
        #     else:
        #         print("注册失败")


import pymysql
from domain.user import user
from web.setting import *


def login(usern, passwd):
    try:
        conn = pymysql.connect(host=host, port=port, db=DB, user=USERNAME, passwd=PASSWD, charset="utf8")
        cr = conn.cursor()
        param = [usern]
        sql = "select id from user where name=%s"
        cr.execute(sql, param)

        name = cr.fetchone()

        if name == None:
            cr.close()
            conn.close()
            return

        sql = "select id,nickname,head from user where name=%s and password=%s"

        param.append(passwd)
        cr.execute(sql, param)
        u = cr.fetchone()

        if not u:
            cr.close()
            conn.close()
            return

        usr = user(u[0], u[1])
        usr.set_head(u[2])

        cr.close()
        conn.close()

        return usr

    except Exception as e:
        print(e)
        print("出现了未知错误")
        return

if __name__ == "__main__":
    x = login("nmszt55", "258330500")
    if not x:
        print("登录失败")
    else:
        print("登录成功")

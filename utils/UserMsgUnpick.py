from web.setting import *
from domain.user import user
import re


def unpick(userstr):
    try:
        ut = userstr.split(USER_SEPARATE)
        ur = user(ut[0], ut[1])
        if not ut[2]:
            ur.set_head(ut[2])
        return ur
    except Exception:
        return None


def friendunpick(friends_str):
    try:
        user_list = []
        analyse_list = friends_str.split(USER_SEPARATE)
        for u in analyse_list:
            if not u:
                break
            u1 = u.split(ATTR_SERARATE)
            usr = user(u1[0], u1[1])
            if not u1[2]:
                usr.set_head(DEFAULT_HEAD)
            user_list.append(usr)
        return user_list
    except Exception as e:
        print("分析朋友出现问题", e)
        return False


def addfriendunpick(user_str):
    try:
        u = user_str.split(ATTR_SERARATE)
        user_ = user(u[0], u[1])
        user_.set_head(u[2])
        return user_
    except Exception as e:
        print("解包出现问题", e)


def msg_devide(data):  # 将发送信息解包 格式:头+地址字符串+发送方id+接收方id+MD5 //msg已经被提取
    try:
        msg = re.findall(MSG_START + r"(.*\n?(.*)?)" + MSG_END, data)[0]
        data = data.replace(MSG_START + msg[0] + MSG_END+SEPARATE, "")
        data = data.split(SEPARATE)
        oid = data[2]
        sid = data[3]
        md5 = data[-1]
        dic = {"oid": oid, "sid": sid, "msg": msg[0], "md5": md5}
        return dic

    except Exception as e:
        print("正则匹配失败", e)
        return False


# 打包发送信息
def send_msg_pack(sid,opid,msg):
    strs = RECEIVE_MSG_HEAD["NEW_MSG_HEAD"] + SEPARATE + sid + SEPARATE + opid + SEPARATE + MSG_START + msg + MSG_END
    return strs.encode()
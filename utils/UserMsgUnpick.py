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
        online_list = []
        analyse_list = friends_str.split(USER_SEPARATE)
        for u in analyse_list:
            if not u:
                break
            u1 = u.split(ATTR_SERARATE)
            usr = user(u1[0], u1[1])
            if not u1[2]:
                usr.set_head(DEFAULT_HEAD)
            # 生成是否在线列表
            if u1[3] == "online":
                online_list.append((u1[0], True))
            else:
                online_list.append((u1[0], False))
            user_list.append(usr)
        return user_list, online_list
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


# 解包信息
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


# 将服务器发送过来的留言信息解包,制作成字典形式返回
def leaving_msg_unpuck(data):
        msg = re.findall(MSG_START + r"(.*\n?(.*)?)" + MSG_END, data)[0][0]
        data = data.replace(MSG_START + msg + MSG_END + SEPARATE, "")

        datalist = data.split(SEPARATE)
        sendtime = datalist[2]
        sid = datalist[3]
        fromid = datalist[4]
        md5 = datalist[5]

        dic = {
            "msg": msg,
            "sid": sid,
            'fromid': fromid,
            "md5": md5,
            "sendtime": sendtime
        }
        return dic


# 判断是否粘包
def is_zhanbao(data):
    pd = 0
    for x in RESPONSE_HEADS.values():
        if x in data:
            pd += data.count(x)
    for x in RECEIVE_MSG_HEAD.values():
        if x in data:
            pd += data.count(x)
    for x in REQUEST_HEADS.values():
        if x in data:
            pd += data.count(x)
    for x in FAILED_HEADS.values():
        if x in data:
            pd += data.count(x)
    if pd > 1:
        print(pd)
        return True
    elif pd == 1:
        return False
    else:
        print("分析粘包的时候出现了非法消息", pd)


def zhanbao_devide(data):
    li = re.split(END_SEPARATE, data)
    return li




if __name__ == "__main__":
    str = """
    <leavingmsg>,176.234.83.81:40130,&start<<sadsdadsadsa&end>>,2018-09-22 21:00:24,2,12,da4b9237bacccdf19c0760cab7aec4a8359010b0<leavingmsg>,176.234.83.81:40130,&start<<dsasdadsadsaf&end>>,2018-09-22 21:00:39,2,12,da4b9237bacccdf19c0760cab7aec4a8359010b0<leavingmsg>,176.234.83.81:40130,&start<<dsdsasdasdadsasda&end>>,2018-09-22 21:00:25,2,12,da4b9237bacccdf19c0760cab7aec4a8359010b0<leavingmsg>,176.234.83.81:40130,&start<<dsadsdsadsasdasda&end>>,2018-09-22 21:00:42,2,12,da4b9237bacccdf19c0760cab7aec4a8359010b0
    """
    for x in zhanbao_devide(str):
        print(x)
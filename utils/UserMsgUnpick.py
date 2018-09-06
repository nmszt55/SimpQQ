from web.setting import *
from domain.user import user

def unpick(userstr):
    try:
        ut = userstr.split(USER_SEPARATE)
        ur = user(ut[0], ut[1])
        if not ut[2]:
            ur.set_head(ut[2])
        return ur
    except Exception as e:
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
        print("解包出现问题",e)
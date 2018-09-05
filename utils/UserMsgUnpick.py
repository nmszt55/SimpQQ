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
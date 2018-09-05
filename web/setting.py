# 地址
SER_HOST = '127.0.0.1'
SER_PORT = 8000
# 定义分隔符
SEPARATE = ","
ATTR_SERARATE = "&"
USER_SEPARATE = "$"
# 默认样式
testBorder = "border-width: 2px;border-style: solid;border-color: 	#3D3D3D;"
DEFAULT_HEAD = '../image/default_user.png'
# 标准消息头
REQUEST_HEADS = {
    "ADD_FRIEND_HEAD": "<addfriend>",
    "LOGIN_HEAD": "<login>",
    "DELETE_HEAD": "<deletefriend>",
    "GET_USER_HEAD": "<getuser>",
    "GET_FRIENDS_HEAD": "<getfriends>",
    "REGISTER_HEAD": "<register>",
    "DISCONNECT_HEAD": "<quit>",
    "SEND_MSG_HEAD": "<sendmsg>"  # 格式:<sendmsg>,sessionid,自己id,目标id,判断session是否正确
}

FAILED_HEADS = {
    "ILLEGAL_HEAD": "<illegalhead>",
    "NO_FRIEND_HEAD": "<nofriends>",
    "NO_USER_HEAD": "<nouser>",
    "DELETE_FRIEND_FAILED_HEAD": "<deletefriendfailed>",
    "REGISTER_FAILED_HEAD": "<registerfailed>",
    "FORM_ERROR": "<formerror>",
    "LOGIN_FAILED": "<loginfailed>",
    "ADD_FRIEND_FAILED": "<addfriendfailed>",
    "FRIEND_ALREADY_EXISTS": "<friendalreadyexists>"
}

RESPONSE_HEADS = {
    "GET_FRIENDS_SUCCESS": "<getfriendssuccess>",
    "GET_USR_SUCCESS": "<getusersuccess>",
    "DELETE_FRIEND_SUCCESS": "<deletefriendsuccess>",
    "REGISTER_SUCCESS": '<registersuccess>',
    "LOGIN_SUCCESS": "<loginsuccess>",
    "ADD_FRIEND_SUCCESS": "<addfriendsuccess>",
}
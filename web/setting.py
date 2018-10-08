# 地址
SER_HOST = '176.234.83.81'
SER_PORT = 7878

# 接收数据大小
MAX_DATA = 2048
# 默认图标
DEFAULT_ICON = "../image/WidgetIcon.png"
# 一次发送文件的大小
MAX_FILESEND = 1024

# charset
CHARSET = "utf-8"

# 定义分隔符
SEPARATE = ","
ATTR_SERARATE = "&"
USER_SEPARATE = "$"
MSG_START = "&start<<"
MSG_END = "&end>>"
END_SEPARATE = "<⊥>"
FILE_SEPARATE = '<◆>'

# 默认样式
testBorder = "border-width: 2px;border-style: solid;border-color: 	#3D3D3D;"
DEFAULT_HEAD = '../image/default_user.png'
# 标准消息头
CLIENT_HEADS = {
    "ADD_FRIEND_IN_LABEL": "<addfriend>",
}
# 记录上次登录用户名的地址
LAST_LOGIN_ADDR = "../LastLogin.txt"

REQUEST_HEADS = {
    "DELETE_CHAT_PORT_HEAD": "<deletechataddr>",
    "ADD_FRIEND_HEAD": "<addfriend>",
    "LOGIN_HEAD": "<login>",
    "DELETE_HEAD": "<deletefriend>",
    "GET_USER_HEAD": "<getuser>",
    "GET_FRIENDS_HEAD": "<getfriends>",
    "REGISTER_HEAD": "<register>",
    "DISCONNECT_HEAD": "<quit>",
    "SEND_MSG_HEAD": "<sendmsg>",  # 格式:<..>
    "CORRECT_ADDR_HEAD": "<correctaddr>",
    "BUILD_ESTABLISH_HEAD": "<chatwidgetsock>",

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
    "FRIEND_ALREADY_EXISTS": "<friendalreadyexists>",
    "SEND_MESSAGE_FAILED": "<sendmsgfailed>",
    "CORRECT_PORT_FAILED": "<changeportfailed>",
    "NOT_ONLINE_ERROR": "<friendnotonline>",
    "BULID_ESTABLISH_FAILED": "<failedtobulidconnection>",
    "CANNOT_ADD_SELF_ERROR": "<cannotaddfriendself>",
}

RESPONSE_HEADS = {
    "GET_FRIENDS_SUCCESS": "<getfriendssuccess>",
    "GET_USR_SUCCESS": "<getusersuccess>",
    "DELETE_FRIEND_SUCCESS": "<deletefriendsuccess>",
    "REGISTER_SUCCESS": '<registersuccess>',
    "LOGIN_SUCCESS": "<loginsuccess>",
    "ADD_FRIEND_SUCCESS": "<addfriendsuccess>",
    "CORRECT_PORT_SUCCESS": "<correctportsuccess>",
    "BULID_ESTABLISH_SUCCESS": "<connectionestablished>",
    "FILE_DOWNLOAD_SUCCESS": "<filesuccessaa>",
    "ONLINE_HEAD": "<nowonline>",
    "UNDERLINE_HEAD": "<nowunderline>"
}

RECEIVE_MSG_HEAD = {
    "NEW_MSG_HEAD": "<newmsg>",  # 格式:<..>,fromid,opid,neirong
    'LEAVE_MSG_HEAD': "<leavingmsg>",  # 格式:<头>,接收地址,格式化消息,发送时间,接收人id,发送人id,MD5
}

OTHER_HEAD = {
    # 提示客户端建立接受文件的socket
    "THIS_IS_FILESOCK_HEAD": "<filesockconnect>",
    # 提示客户端接收很多文件
    "NEED_TO_RECV_FILES_HEAD": "<needrecvmanyfile>",
    # 带着文件信息发送到文件sock
    "FILE_INF_HEAD": "<fileinformation>",
    # 需要接收单个文件
    "NEED_TO_RECV_FILE_HEAD": "<usockneedrecvfile>",
}
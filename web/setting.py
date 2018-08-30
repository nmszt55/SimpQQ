
host = '127.0.0.1'
port = 3306
DB = 'user'
USERNAME = "QQserver"
PASSWD = "123456"
testBorder = "border-width: 2px;border-style: solid;border-color: 	#3D3D3D;"
default_head = '../image/default_user.png'

friendsql = "SELECT DISTINCT id,nickname,head FROM user" \
            " INNER JOIN friend on friend.uid1 = user.id or friend.uid2 = user.id" \
            " where (friend.uid1 = %s or friend.uid2 = %s) and id != %s"

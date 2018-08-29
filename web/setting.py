
host = '127.0.0.1'
port = 3306
DB = 'user'
USERNAME = "QQserver"
PASSWD = "123456"

friendsql = "SELECT DISTINCT id,nickname,head FROM user" \
            " INNER JOIN friend on friend.uid1 = user.id or friend.uid2 = user.id" \
            " where (friend.uid1 = %s or friend.uid2 = %s) and id != %s"

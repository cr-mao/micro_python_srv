from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


# 连接池
# ReconnectMixin 防止连接断开
class ReconnectMysqlDATABASE(ReconnectMixin, PooledMySQLDatabase):
    pass


MYSQL_DB = "micro_user_srv"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""

# super -> PooledMySQLDatabase
DB = ReconnectMysqlDATABASE(MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, password=MYSQL_PASSWORD, user=MYSQL_USER)

CONSUL_HOST = "127.0.0.1"
CONSUL_PORT = 8500

# 服务相关配置
SERVICE_NAME = "user-srv"
SERVICE_ID = "user-srv"
SERVICE_TAG = ["python-srv"]


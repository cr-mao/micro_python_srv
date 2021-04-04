import nacos
import json
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


# 连接池
# ReconnectMixin 防止连接断开
class ReconnectMysqlDATABASE(ReconnectMixin, PooledMySQLDatabase):
    pass


NACOS = {
    "Host": "127.0.0.1",
    "Port": 8848,
    "NameSpace": "f59db538-cb44-45e0-96fd-3f4262e37e5b",
    "User": "nacos",
    "Password": "nacos",
    "DataId": "python-user-srv.json",
    "Group": "dev",
}
SERVER_ADDRESSES = f"http://{NACOS['Host']}:{NACOS['Port']}"
NAMESPACE = NACOS["NameSpace"]
data_id = NACOS["DataId"]
group = NACOS["Group"]

configs = {
    "mysql": {
        "db": "micro_user_srv",
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": ""
    },
    "consul": {
        "host": "127.0.0.1",
        "port": 8500
    },
    "service_name": "user-srv",
    "service_tag": ["python-srv1"],
    "redis": {
        "host": "127.0.0.1",
        "port": 6379,
        "db": 0
    }
}


def config_change_callback(args):
    global configs
    configs = json.loads(args["raw_content"])




# 手动开关 默认开启nacos
if True:
    nacosClient = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)
    configs = nacosClient.get_config(data_id, group)
    configs = json.loads(configs)

MYSQL_DB = configs["mysql"]["db"]
MYSQL_HOST = configs["mysql"]["host"]
MYSQL_PORT = configs["mysql"]["port"]
MYSQL_USER = configs["mysql"]["user"]
MYSQL_PASSWORD = configs["mysql"]["password"]
# super -> PooledMySQLDatabase
DB = ReconnectMysqlDATABASE(MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, password=MYSQL_PASSWORD, user=MYSQL_USER)
CONSUL_HOST = configs["consul"]["host"]
CONSUL_PORT = configs["consul"]["port"]

# consul 服务相关配置
SERVICE_NAME = configs["service_name"]
SERVICE_ID = "user-srv"  # 作废 ，无用了
SERVICE_TAG = configs["service_tag"]

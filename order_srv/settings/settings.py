import nacos
import json
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
import redis


# 连接池
# ReconnectMixin 防止连接断开
class ReconnectMysqlDATABASE(ReconnectMixin, PooledMySQLDatabase):
    pass


NACOS = {
    "Host": "127.0.0.1",
    "Port": 8848,
    "NameSpace": "df0238af-c0eb-470a-9395-23dee67bdc97",
    "User": "nacos",
    "Password": "nacos",
    "DataId": "python-order-srv.json",
    "Group": "dev",
}
SERVER_ADDRESSES = f"http://{NACOS['Host']}:{NACOS['Port']}"
NAMESPACE = NACOS["NameSpace"]
data_id = NACOS["DataId"]
group = NACOS["Group"]

configs = {
    "mysql": {
        "db": "micro_order_srv",
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": ""
    },
    "consul": {
        "host": "127.0.0.1",
        "port": 8500
    },
    "service_name": "order_srv",
    "service_tag": ["order_srv_tag"],
    "redis": {
        "host": "127.0.0.1",
        "port": 6379,
        "db": 0
    },
    "goods_srv": {
        "name": "goods-srv"
    },
    "inventory_srv": {
        "name": "inventory-srv"
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
# redis
# REDIS_HOST = configs["redis"]["host"]
# REDIS_PORT = configs["redis"]["port"]
# REDIS_DB = configs["redis"]["db"]
# pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
# REDIS_CLIENT = redis.StrictRedis(connection_pool=pool)

# consul 服务相关配置
SERVICE_NAME = configs["service_name"]
SERVICE_TAG = configs["service_tag"]

GOODS_SRV_NAME = configs["goods_srv"]["name"]
INVENTORY_SRV_NAME = configs["inventory_srv"]["name"]

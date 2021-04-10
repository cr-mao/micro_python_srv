# micro_python_srv

a simple shop project python services 

Python版本要求为 Python-3.6.x

```
├── build 
     ├── rocketmq docker-compose安装方式
├── order_srv 订单服务
├── inventory_srv 库存服务
├── goods_srv 商品服务
├── user_srv  用户服务
    ├── proto proto相关文件
    ├── settings 配置初始化
    ├── models 存放模型相关
    ├── handler 编写具体service 
    └── tests 测试用例
├── nacos  nacos操作库 
├── scipts 快捷命令、启动入口
├── common
    ├── grpc_health grpc健康监测
    ├── register    服务注册类库
    ├── lock        分布锁库


    
```

技术选型
- server: grpc server 
- 日志库：loguru
- orm:   peewee
- 服务注册 consul 
- 配置中心 [nacos](https://github.com/nacos-group/nacos-sdk-python) 
- mq:     rocketmq



### Quick Start



- 环境
```
# 初始化
$ python3.6 -m venv .virtualenv

# 安装依赖
$ make

# 修改配置
 user_srv/settings/settings.py 
 goods_srv/settings/settings.py
 inventory_srv/settings/settings.py
 order_srv/settings/settings.py    

# 初始化表，库手动创建
user_srv/models/models.py
goods_srv/models/models.py
inventory_srv/models/models.py
order_srv/models/models.py


#本地启动consul
$ consul agent -dev
 

#启动nacos
$ docker run --name nacos-standalone -e MODE=standalone -e JVM_XMS=512m -e JVM_XMX=512m -e JVM_XMN=256m -p 8848:8848 -d nacos/nacos-server:latest

# 启动jaeger 
$ docker run --rm --name jaeger  -p6831:6831/udp  -p16686:16686  jaegertracing/all-in-one:latest

```



- 运行

```
$ make user_serve
$ make goods_serve
$ make inventory_serve
$ make order_serve

或者 
python user_srv/server.py --ip=xxx --port=xxx
python goods_srv/server.py --ip=xxx --port=xxx
python inventory_srv/server.py --ip=xxx --port=xxx
python order_srv/server.py --ip=xxx --port=xxx

```

- proto文件生成命令
```
 make codegen
```




#### 其他说明
```
启动服务，服务端口随机生成，向consul注册服务的时候，server_id也是随机生成
用于多实例负载均衡
```













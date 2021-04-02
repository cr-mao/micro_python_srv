# micro_python_srv

python services 

Python版本要求为 Python-3.6.x

```
├── user_srv  用户微服务
    ├── proto proto相关文件
    ├── settings 配置初始化
    ├── models 存放模型相关
    ├── handler 编写具体service 如userService
    └── tests 测试用例
├── nacos  
├── scipts 快捷命令、启动入口
├── common
    ├── grpc_health grpc健康监测
    ├── register    服务注册类库

    
```

技术选型
- server: grpc server 
- 日志库：loguru
- orm:   peewee
- 服务注册 consul 
- 配置中心 [nacos](https://github.com/nacos-group/nacos-sdk-python) 


### Quick Start

- 配置文件
  
   
- 


- 环境
```
# 初始化
$ python3.6 -m venv .virtualenv

# 安装依赖
$ make

# 配置文件
 user_srv/settings/settings.py 
 依赖consul和mysql 
 先创建库

#初始化表，数据
见user_srv/models/models.py

#本地启动consul
$ consul agent -dev
 

#启动nacos
$ docker run --name nacos-standalone -e MODE=standalone -e JVM_XMS=512m -e JVM_XMX=512m -e JVM_XMN=256m -p 8848:8848 -d nacos/nacos-server:latest
```

- 运行

```
# 启动服务
$ make serve
或者 
python user_srv/server.py --ip=xxx --port=xxx
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













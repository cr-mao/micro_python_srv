# micro_python_srv

python端微服务

Python版本要求为 Python-3.6.x

```
├── user_srv  用户微服务
    ├── proto proto相关文件
    ├── settings 配置初始化
    ├── models 存放模型相关
    ├── handler 编写具体service 如userService
    └── tests 测试用例

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


### Quick Start

- 配置文件

   user_srv/settings/settings.py
   
  依赖consul和mysql

- 环境
```
# 初始化
$ python3.6 -m venv .virtualenv

# 安装依赖
$ make
```

- 运行

```
# 启动服务
$ make serve
或者 
python user_srv/server.py --ip=xxx --port=xxx
```


### 便捷
- proto文件生成命令
```
 make codegen
```















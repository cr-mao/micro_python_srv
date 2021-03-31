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
```

技术选型
- server: grpc server 
- 日志库：loguru
- orm:   peewee


### Quick Start

- 配置文件
    - 项目根目录下的 `config.py` **放一些基础的配置项目，比如建立新配置**
    - 项目根目录下的 `config_local.py` **放开发人员本地的不同配置，不进版本管理**

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













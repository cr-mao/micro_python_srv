import os
import argparse
import socket
import sys
from concurrent import futures
import signal
import grpc
from loguru import logger
from functools import partial
import uuid

# 解决 自动生成 proto 文件  模块导入问题
from common.register import consul
from user_srv.settings import settings

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
PROTO_DIR = ROOT_PATH + '/proto'
sys.path.append(PROTO_DIR)


# 日志拦截器
class LogInterceptors(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        # print("请求start")
        # print(type(handler_call_details))
        resp = continuation(handler_call_details)
        # print("请求end")
        return resp


def on_exit(signo, frame, server_id):
    """
    信号回调函数
    :param signo:
    :param frame:
    :return:
    """
    # 删除注册服务
    register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
    logger.info(f"删除服务,service_id: {server_id}")
    register.deregister(server_id)
    logger.info("进程中断")
    sys.exit(0)


def get_free_tcp_port():
    """
    动态获得port
    :return:
    """
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port


class Applicaton():
    def __init__(self):
        pass

    def serve(self):
        from user_srv.proto import user_pb2_grpc
        from common.grpc_health.v1 import health_pb2_grpc, health
        from user_srv.handler.user import UserServicer

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(LogInterceptors(),))
        user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
        # https://www.consul.io/api-docs/agent/check#grpcusetls
        # grpc 健康监测服务
        health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", nargs="?", type=str, default="127.0.0.1", help="bingding ip")
        parser.add_argument("--port", nargs="?", type=int, default=0, help="server port")
        args = parser.parse_args()
        # 服务端口也随机生成
        port = args.port
        if args.port == 0:
            port = get_free_tcp_port()

        server.add_insecure_port(f"{args.ip}:{port}")

        """
            sigint CTRL+C
            sigterm kill 
        """
        server_id = str(uuid.uuid4())
        # 包装函数 传递更多的参数
        signal.signal(signal.SIGINT, partial(on_exit, server_id=server_id))
        signal.signal(signal.SIGTERM, partial(on_exit, server_id=server_id))

        logger.info(f"启动服务:{args.ip}:{port}")
        server.start()
        logger.info("服务注册开始")
        #  向consul 注册服务
        register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
        # server_id  随机生成
        if not register.register(settings.SERVICE_NAME, server_id, args.ip, port,
                                 settings.SERVICE_TAG):
            logger.info("服务注册失败")
            sys.exit(0)
        logger.info("服务注册成功")

        server.wait_for_termination()


app = Applicaton()

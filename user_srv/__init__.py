import os
import argparse
import sys
from concurrent import futures
import signal
import grpc
from loguru import logger

# 解决 自动生成 proto 文件  模块导入问题

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
PROTO_DIR = ROOT_PATH + '/proto'
sys.path.append(PROTO_DIR)


# 日志拦截器
class LogInterceptors(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        print("请求start")
        # print(type(handler_call_details))
        resp = continuation(handler_call_details)
        print("请求end")
        return resp


# 信号回调函数
def on_exit(signo, frame):
    logger.info("进程中断")
    sys.exit(0)


class Applicaton():
    def __init__(self):
        pass

    def serve(self):
        from user_srv.proto import user_pb2, user_pb2_grpc

        from common.grpc_health.v1 import health_pb2, health_pb2_grpc,health

        from user_srv.handler.user import UserServicer

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(LogInterceptors(),))
        user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)


        #https://www.consul.io/api-docs/agent/check#grpcusetls
        # grpc 健康监测
        health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)

        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", nargs="?", type=str, default="127.0.0.1", help="bingding ip")
        parser.add_argument("--port", nargs="?", type=int, default="50052", help="server port")
        args = parser.parse_args()

        server.add_insecure_port(f"{args.ip}:{args.port}")

        """
            sigint CTRL+C
            sigterm kill 
        """
        signal.signal(signal.SIGINT, on_exit)
        signal.signal(signal.SIGTERM, on_exit)

        logger.info(f"启动服务:{args.ip}:{args.port}")
        server.start()
        server.wait_for_termination()


app = Applicaton()

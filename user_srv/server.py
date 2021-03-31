from concurrent import futures
import logging

import grpc

from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.handler.user import UserServicer



# 日志拦截器
class LogInterceptors(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        print("请求start")
        # print(type(handler_call_details))
        resp = continuation(handler_call_details)
        print("请求end")
        return resp


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(LogInterceptors(),))
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    server.add_insecure_port('[::]:50052')
    print(f"启动服务:127.0.0.1:50052")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    # print("start")
    serve()

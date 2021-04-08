import random

import requests

from common.register import base

import consul


class ConsulRegister(base.Register):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.c = consul.Consul(host=host, port=port)

    def register(self, name, id, address, port, tag, check=None):
        """
        注册服务
        :param name:
        :param id:
        :param address:
        :param port:
        :return:
        """
        if check is None:
            check = {
                "GRPC": f"{address}:{port}",
                "GRPCUseTLS": False,
                "Timeout": "5s",
                "Interval": "5s",
                "DeregisterCriticalServiceAfter": "15s",
            }
        else:
            check = check

        success = self.c.agent.service.register(name=name,
                                                service_id=id,
                                                address=address,
                                                port=port,
                                                tags=tag,
                                                check=check)
        return success

    def deregister(self, service_id):
        """
        注销服务
        :param service_id:
        :return:
        """
        return self.c.agent.service.deregister(service_id)

    def get_all_service(self):
        """
        获得所有服务
        """
        return self.c.agent.services()

    def filter_service(self, filter):
        """
        过滤获得服务
        :param filter:
        :return:
        """
        url = f"http://{self.host}:{self.port}/v1/agent/services"
        params = {
            "filter": filter
        }
        rsp = requests.get(url, params=params).json()
        return rsp

    def get_host_port(self, filter):
        """
        根据filter 获得 host，port
        :param filter:
        :return:
        """
        url = f"http://{self.host}:{self.port}/v1/agent/services"
        params = {
            "filter": filter
        }
        data = requests.get(url, params=params).json()
        if data:
            service_info = random.choice(list(data.values()))
            return service_info["Address"], service_info["Port"]
        return None, None

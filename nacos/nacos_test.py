import nacos

# Both HTTP/HTTPS protocols are supported, if not set protocol prefix default is HTTP, and HTTPS with no ssl check(verify=False)
# "192.168.3.4:8848" or "https://192.168.3.4:443" or "http://192.168.3.4:8848,192.168.3.5:8848" or "https://192.168.3.4:443,https://192.168.3.5:443"
SERVER_ADDRESSES = "http://127.0.0.1:8848"
NAMESPACE = "f59db538-cb44-45e0-96fd-3f4262e37e5b"








def test_cb(args):
    print("配置文件更新")
    print(args)


if __name__ == "__main__":
    # no auth mode
    client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)
    # auth mode
    # client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, username="nacos", password="nacos")
    # get config
    data_id = "config-debug.yaml"
    group = "dev"
    print(client.get_config(data_id, group))
    # 文档有点错误，  回调函数 必须是 列表形式  ,下面方式报错
    #     client.add_config_watchers(data_id, group, test_cb)
    client.add_config_watchers(data_id, group, [test_cb])
    import time

    time.sleep(3000)

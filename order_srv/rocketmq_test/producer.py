import time
from rocketmq.client import Producer, Message, TransactionMQProducer, TransactionStatus

topicTest = "hellomq"


# https://github.com/apache/rocketmq-client-python


def check_callback(msg):
    # TransactionStatus.COMMIT,TransactionStatus.ROLLBACK,TransactionStatus.UNKNOWN
    print("事务消息回查")
    print(f"事务消息回查:{msg.body.decode('utf-8')}")
    return TransactionStatus.COMMIT


def local_execute(msg, user_args):
    # TransactionStatus.COMMIT,TransactionStatus.ROLLBACK,TransactionStatus.UNKNOWN
    # 执行业务逻辑，如 订单表插入
    print("执行本地事务逻辑")
    # TransactionStatus.UNKNOWN 进行回查
    return TransactionStatus.UNKNOWN


def create_delay_message():
    msg = Message(topicTest)
    msg.set_keys("crmao_key")
    msg.set_tags("crmao")
    msg.set_delay_time_level(2)  # 1s 5s ......        16个级别
    msg.set_property("name", "micro services")
    msg.set_body("hello rocketmq")
    return msg


def create_message():
    msg = Message(topicTest)
    msg.set_keys("crmao_key")
    msg.set_tags("crmao")
    # msg.set_delay_time_level(2)  # 1s 5s ......        16个级别
    msg.set_property("name", "micro services")
    msg.set_body("hello rocketmq")
    return msg


def send_transaction_message(count):
    producer = TransactionMQProducer("test", check_callback)
    # nameserver
    producer.set_name_server_address("127.0.0.1:9876")
    #  首先启动producer
    producer.start()

    for n in range(count):
        msg = create_message()
        ret = producer.send_message_in_transaction(msg, local_execute, None)
        print(f"发送状态:{ret.status},消息id:{ret.msg_id}")

    print("消息发送完成")
    while True:
        time.sleep(3600)
    #



def send_message_sync(count):
    producer = Producer("test")
    # nameserver
    producer.set_name_server_address("127.0.0.1:9876")
    #  首先启动producer
    producer.start()

    for n in range(count):
        msg = create_message()
        ret = producer.send_sync(msg)
        print(f"发送状态:{ret.status},消息id:{ret.msg_id}")

    print("消息发送完成")
    producer.shutdown()


if __name__ == "__main__":
    # send_message_sync(10)
    # 发送事务消息
    send_transaction_message(5)

from rocketmq.client import Producer, Message

topicTest = "hellomq"


# https://github.com/apache/rocketmq-client-python

def create_message():
    msg = Message(topicTest)
    msg.set_keys("crmao_key")
    msg.set_tags("crmao")
    msg.set_property("name", "micro services")
    msg.set_body("hello rocketmq")
    return msg


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
    send_message_sync(10)

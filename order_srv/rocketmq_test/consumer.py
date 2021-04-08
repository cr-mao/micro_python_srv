import time

from rocketmq.client import PushConsumer, ConsumeStatus


# https://github.com/apache/rocketmq-client-python
def callback(msg):
    print(msg.id, msg.body)
    return ConsumeStatus.CONSUME_SUCCESS


consumer = PushConsumer('CID_XXX')
consumer.set_name_server_address('127.0.0.1:9876')
consumer.subscribe('hellomq', callback)
consumer.start()

while True:
    time.sleep(3600)

consumer.shutdown()

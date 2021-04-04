import uuid
import redis


class Lock:
    def __init__(self, name, id=None):
        self.id = uuid.uuid4()
        self.redis_client = redis.Redis(host="127.0.0.1")
        self.name = name

    def acquire(self):
        """
        加锁
        :return:
        """
        if self.redis_client.set(self.name, self.id, nx=True, ex=15):
            # 启动一个线程，定时刷新过期时间，这个操作最好也是使用lua 来完成
            return True
        else:
            while True:
                import time
                time.sleep(1)
                if self.redis_client.set(self.name, 1, nx=True, ex=15):
                    return True

    def release(self):
        """
        释放锁
        :return:
        """
        # 先做一个判断，先取出值来然后判断当前的值和自己的lock中的值是否相等，相等才可以删除
        # lua 去做
        id = self.redis_client.get(self.name)
        if id == self.id:
            self.redis_client.delete(self.name)
        else:
            print("不能删除不属于自己的锁")

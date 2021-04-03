import grpc

from goods_srv.proto import goods_pb2, goods_pb2_grpc


class GoodsTest:
    def __init__(self):
        channel = grpc.insecure_channel("127.0.0.1:50975")
        self.stub = goods_pb2_grpc.GoodsStub(channel)

    def goods_list(self):
        rsp: goods_pb2.GoodsListResponse = self.stub.GoodsList(goods_pb2.GoodsFilterRequest())
        print(rsp.total)
        print(rsp.goods)
        for g in rsp.goods:
            print(g.name)

    def batch_get(self):
        request = goods_pb2.BatchGoodsIdInfo()
        request.id.extend([1])
        rsp: goods_pb2.GoodsListResponse = self.stub.BatchGetGoods(
            request=request
        )
        print(rsp.total)
        for good in rsp.goods:
            print(good)


if __name__ == "__main__":
    goods = GoodsTest()
    # goods.goods_list()
    goods.batch_get()

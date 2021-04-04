import grpc

from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc


class InventoryTest:
    def __init__(self):
        channel = grpc.insecure_channel("127.0.0.1:51899")
        self.stub = inventory_pb2_grpc.InventoryStub(channel)

    def set_inv(self):
        """
        设置库存
        :return:
        """
        rsp = self.stub.SetInv(
            inventory_pb2.GoodsInvInfo(
                goodsId=1, num=20
            )
        )
        print(rsp)

    def get_inv(self):
        """
        获得库存
        :return:
        """
        rsp = self.stub.InvDetail(
            inventory_pb2.GoodsInvInfo(goodsId=1)
        )
        print(rsp)

    def sell(self):
        """
        扣库存
        :return:
        """
        request = inventory_pb2.SellInfo()
        request.goodsInfo.append(inventory_pb2.GoodsInvInfo(
            goodsId=1, num=3
        ))
        rsp = self.stub.Sell(
            request=request
        )
        print(rsp)

    def reback(self):
        goods_list = [(1, 3)]
        request = inventory_pb2.SellInfo()
        for goodsId, num in goods_list:
            request.goodsInfo.append(inventory_pb2.GoodsInvInfo(
                goodsId=1, num=3
            ))
        rsp = self.stub.Reback(request=request)


if __name__ == "__main__":
    inventory = InventoryTest()
    # inventory.set_inv()
    # inventory.get_inv()
    inventory.sell()
    # inventory.reback()

import grpc
from google.protobuf import empty_pb2
from loguru import logger
from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc
from inventory_srv.model.models import Inventory, DoesNotExist
from inventory_srv.settings import settings


class InventoryServicer(inventory_pb2_grpc.InventoryServicer):

    @logger.catch
    def SetInv(self, request: inventory_pb2.GoodsInvInfo, context):
        """
        插入或者更新库存
        :param request:
        :param context:
        :return:
        """
        force_insert = False

        invs = Inventory.select().where(Inventory.goods == request.goodsId)
        if not invs:
            inv = Inventory()
            inv.goods = request.goodsId
            force_insert = True
        else:
            inv = invs[0]
        inv.stocks = request.num
        inv.save(force_insert=force_insert)
        return empty_pb2.Empty()

    @logger.catch
    def InvDetail(self, request, context):
        """
        获得库存
        :param request:
        :param context:
        :return:
        """
        try:
            inv = Inventory.get(Inventory.goods == request.goodsId)
            return inventory_pb2.GoodsInvInfo(
                goodsId=inv.goods,
                num=inv.stocks
            )
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("没有库存记录")

    @logger.catch
    def Sell(self, request, context):
        """
        扣减库存,超卖问题，事务
        :param request:
        :param context:
        :return:
        """
        # 事务
        with settings.DB.atomic() as txn:
            for item in request.goodsInfo:
                try:
                    goods_inv = Inventory.get(Inventory.goods == item.goodsId)
                except DoesNotExist as e:
                    txn.rollback()
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("id有误")
                    return empty_pb2.Empty()
                if goods_inv.stocks < item.num:
                    txn.rollback()
                    context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
                    context.set_details("库存不足")
                    return empty_pb2.Empty()
                else:
                    goods_inv.stocks -= item.num
                    goods_inv.save()
        return empty_pb2.Empty()

    @logger.catch
    def Reback(self, request: inventory_pb2.GoodsInvInfo, context):
        """
         # 1. 订单超时，2. 订单创建失败 3.手动归还
        :param request:
        :param context:
        :return:
        """
        with settings.DB.atomic() as txn:
            for item in request.goodsInfo:
                try:
                    goods_inv = Inventory.get(Inventory.goods == item.goodsId)
                except DoesNotExist as e:
                    txn.rollback()
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("id有误")
                    return empty_pb2.Empty()
                # 可能数据不一致
                goods_inv.stocks += item.num
                goods_inv.save()
        return empty_pb2.Empty()

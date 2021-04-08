import grpc
from google.protobuf import empty_pb2
from loguru import logger
from order_srv.proto import order_pb2_grpc, order_pb2, goods_pb2, goods_pb2_grpc, inventory_pb2, inventory_pb2_grpc
from order_srv.model.models import ShoppingCart, OrderGoods, OrderInfo
from peewee import DoesNotExist
from order_srv.proto import order_pb2

from common.register import consul
from order_srv.settings import settings
import time


def genderate_order_sn(user_id):
    # 当前时间+ user_id+随机数
    import random
    order_sn = f'{time.strftime("%H%m%d%H%M%S")}{user_id}{random.randint(10, 99)}'
    return order_sn


class OrderServicer(order_pb2_grpc.OrderServicer):

    @logger.catch
    def CartItemList(self, request, context):
        """
        用户购物车
        :param request:
        :param context:
        :return:
        """
        items = ShoppingCart.select().where(ShoppingCart.user == request.id)
        rsp = order_pb2.CartItemListResponse(total=items.count())
        for item in items:
            item_rsp = order_pb2.ShopCartInfoResponse()
            item_rsp.id = item.id
            item_rsp.userId = item.user
            item_rsp.goodsId = item.goods
            item_rsp.nums = item.nums
            item_rsp.checked = item.checked
            rsp.data.append(item_rsp)
        return rsp

    @logger.catch
    def CreateCartItem(self, request, context):
        """
        添加商品到购物车
        :param request:
        :param context:
        :return:
        """
        existed_items = ShoppingCart.select().where(ShoppingCart.goods == request.goodsId,
                                                    ShoppingCart.user == request.userId)

        if existed_items:
            item = existed_items[0]
            item.nums += request.nums
        else:
            item = ShoppingCart()
            item.user = request.userId
            item.goods = request.goodsId
            item.nums = request.nums
        item.save()
        return order_pb2.ShopCartInfoResponse(id=item.id)

    @logger.catch
    def UpdateCartItem(self, request, context):
        """
        更新购物车条目， 数量和选中
        :param request:
        :param context:
        :return:
        """
        try:
            item = ShoppingCart.get(ShoppingCart.id == request.id)
            item.checked = request.checked
            if request.nums:
                item.nums = request.nums
            item.save()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("购物车记录不存在")
            return empty_pb2.Empty()

    @logger.catch
    def DeleteCartItem(self, request, context):
        """
        删除购物车条目
        :param request:
        :param context:
        :return:
        """
        try:
            item = ShoppingCart.get(ShoppingCart.id == request.id)
            item.delete_instance()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("购物车记录不存在")
            return empty_pb2.Empty()

    def OrderList(self, request, context):
        """
        订单列表
        :param request:
        :param context:
        :return:
        """
        rsp = order_pb2.OrderListResponse()
        orders = OrderInfo.select()
        if request.userId:
            orders = orders.where(OrderInfo.user == request.userId)

        rsp.total = orders.count()
        per_page_nums = request.pagePerNums if request.pagePerNums else 10
        start = per_page_nums * (request.pages - 1) if request.pages else 0
        orders = orders.limit(per_page_nums).offset(start)
        for order in orders:
            tmp_rsp = order_pb2.OrderInfoResponse()
            tmp_rsp.id = order.id
            tmp_rsp.userId = order.user
            tmp_rsp.orderSn = order.order_sn
            tmp_rsp.payType = order.pay_type
            tmp_rsp.status = order.status
            tmp_rsp.post = order.post
            tmp_rsp.total = order.order_mount
            tmp_rsp.address = order.address
            tmp_rsp.name = order.signer_name
            tmp_rsp.mobile = order.signer_mobile
            tmp_rsp.addTime = order.add_time.strftime("%Y-%m-%d %H:%M:%S")
            rsp.data.append(tmp_rsp)
        return rsp

    @logger.catch
    def OrderDetail(self, request, context):
        rsp = order_pb2.OrderInfoDetailResponse()

        try:
            order = OrderInfo.get(OrderInfo.id == request.id)
            rsp.orderInfo.id = order.id
            rsp.orderInfo.userId = order.user
            rsp.orderInfo.orderSn = order.order_sn
            rsp.orderInfo.payType = order.pay_type
            rsp.orderInfo.status = order.status
            rsp.orderInfo.post = order.post
            rsp.orderInfo.total = order.order_mount
            rsp.orderInfo.address = order.address
            rsp.orderInfo.name = order.signer_name
            rsp.orderInfo.mobile = order.signer_mobile
            order_goods = OrderGoods.select().where(OrderGoods.order == order.id)
            for order_good in order_goods:
                order_goods_rsp = order_pb2.OrderItemResponse()
                order_goods_rsp.goodsId = order_good.goods
                order_goods_rsp.goodsName = order_good.goods_name
                order_goods_rsp.goodsImage = order_good.goods_image
                order_goods_rsp.goodsPrice = order_good.goods_price
                order_goods_rsp.nums = order_good.nums
                rsp.goods.append(order_goods_rsp)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("订单记录不存在")
            return rsp

    @logger.catch
    def UpdateOrderStatus(self, request, context):
        """
        更新订单的支付状态
        :param request:
        :param context:
        :return:
        """
        OrderInfo.update(status=request.status).where(OrderInfo.order_sn == request.orderSn).execute()
        return empty_pb2.Empty()

    @logger.catch
    def CreateOrder(self, request, context):
        """
        新建订单
        1. 价格 -访问商品服务
        2. 库存的扣减 -访问库存服务
        3. 订单基本信息表 - 订单的商品信息表
        4. 从购物车获取选中的商品
        5. 从购物车中删除已购买的商品
        :param request:
        :param context:
        :return:
        """

        with settings.DB.atomic() as txn:
            goods_ids = []
            goods_nums = {}
            order_goods_list = []
            order_amount = 0
            goods_sell_info = []
            for cart_item in ShoppingCart.select().where(ShoppingCart.user == request.userId,
                                                         ShoppingCart.checked == 1):
                goods_ids.append(cart_item.goods)
                goods_nums[cart_item.goods] = cart_item.nums
            if not goods_ids:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("没有选中的商品")
                return order_pb2.OrderInfoResponse()

            # 查询商品信息
            register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
            goods_srv_host, goods_srv_port = register.get_host_port(f'Service=="{settings.GOODS_SRV_NAME}"')
            if not goods_srv_host:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("商品服务不可用")
                return order_pb2.OrderInfoResponse()
            goods_channel = grpc.insecure_channel(f"{goods_srv_host}:{goods_srv_port}")
            goods_stub = goods_pb2_grpc.GoodsStub(goods_channel)
            # 批量获取商品的信息
            try:
                goods_info_rsp = goods_stub.BatchGetGoods(goods_pb2.BatchGoodsIdInfo(id=goods_ids))
            except grpc.RpcError as e:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"商品服务不可用{str(e)}")
                return order_pb2.OrderInfoResponse()

            for goods_info in goods_info_rsp.goods:
                order_amount += goods_info.shopPrice * goods_nums[goods_info.id]
                order_goods = OrderGoods(goods=goods_info.id, goods_name=goods_info.name,
                                         goods_image=goods_info.goodsFrontImage,
                                         goods_price=goods_info.shopPrice,
                                         nums=goods_nums[goods_info.id]
                                         )
                order_goods_list.append(order_goods)
                goods_sell_info.append(inventory_pb2.GoodsInvInfo(goodsId=goods_info.id, num=goods_nums[goods_info.id]))

            # 扣减库存
            # 这里要负载均衡吗? dns的resolver 还没有做到维护连接
            inv_srv_host, inv_srv_port = register.get_host_port(f'Service=="{settings.INVENTORY_SRV_NAME}"')
            if not inv_srv_host:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("库存服务不可用")
                return order_pb2.OrderInfoResponse()
            inv_channel = grpc.insecure_channel(f"{inv_srv_host}:{inv_srv_port}")
            inv_stub = inventory_pb2_grpc.InventoryStub(inv_channel)

            try:
                inv_stub.Sell(inventory_pb2.SellInfo(goodsInfo=goods_sell_info))
            except grpc.RpcError as e:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"扣减库存失败{str(e)}")
                return order_pb2.OrderInfoResponse()

            # 创建订单
            try:
                order = OrderInfo()
                order.user = request.userId
                order.order_sn = genderate_order_sn(request.userId)
                order.order_mount = order_amount
                order.address = request.address
                order.signer_name = request.name
                order.signer_mobile = request.mobile
                order.post = request.post
                order.save()

                # 批量插入订单商品表
                for order_good in order_goods_list:
                    order_good.order = order.id
                OrderGoods.bulk_create(order_goods_list)

                # 删除购物车的记录
                ShoppingCart.delete().where(ShoppingCart.user == request.userId,
                                            ShoppingCart.checked == 1).execute()

            except grpc.RpcError as e:
                txn.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"订单创建失败{str(e)}")
                return order_pb2.OrderInfoResponse()

        return order_pb2.OrderInfoResponse(id=order.id, orderSn=order.order_sn, total=order_amount)

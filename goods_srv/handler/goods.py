from loguru import logger

from goods_srv.model.models import Goods, Category
from goods_srv.proto import goods_pb2, goods_pb2_grpc


class GoodsServicer(goods_pb2_grpc.GoodsServicer):
    """
     int32  priceMin = 1;
  int32  priceMax = 2;
  bool isHot = 3;
  bool isNew = 4;
  bool isTab = 5;
  int32 topCategroy = 6;
  int32 pages = 7;
  int32 pagePerNums = 8;
  string keyWords = 9;
  int32 brand = 10;


   int32 id = 1;
  int32  categoryId = 2;
  string name = 3;
  string goodsSn = 4;
  int32 clickNum = 5;
  int32  soldNum = 6;
  int32  favNum = 7;
  float marketPrice = 9;
  float shopPrice = 10;
  string goodsBrief = 11;
  string goodsDesc = 12;
  bool shipFree = 13;
  repeated string images = 14;
  repeated string descImages = 15;
  string goodsFrontImage = 16;
  bool isNew = 17;
  bool isHot = 18;
  bool onSale = 19;
  int64  addTime = 20;
  CategoryBriefInfoResponse category = 21;
  BrandInfoResponse brand = 22;
    """

    def convert_model_to_message(self, goods):
        info_rsp = goods_pb2.GoodsInfoResponse()
        info_rsp.id = goods.id
        info_rsp.categoryId = goods.category.id
        info_rsp.name = goods.name
        info_rsp.shopPrice = goods.shop_price
        info_rsp.descImages.extend(goods.desc_images)
        info_rsp.images.extend(goods.images)
        info_rsp.category.id = goods.category.id
        info_rsp.category.name = goods.category.name
        return info_rsp
        # ...

    @logger.catch
    def GoodsList(self, request: goods_pb2.GoodsFilterRequest, context):
        rsp = goods_pb2.GoodsListResponse()
        goods = Goods.select()
        if request.keyWords:
            goods = goods.filter(Goods.name.contains(request.keyWords))
        if request.topCategroy:
            try:
                ids = []
                category = Category.get(Category.id == request.topCategroy)
                level = category.level
                if level == 1:
                    c2 = Category.alias()
                    categorys = Category.select().where(
                        Category.parent_category.in_(c2.select(c2.id).where(c2.parent_category == request.topCategory)))
                    for category in categorys:
                        ids.append(category.id)
                elif level == 2:
                    categorys = Category.select().where(Category.parent_category == request.topCategory)
                    for category in categorys:
                        ids.append(category.id)
                elif level == 3:
                    ids.append(request.TopCategroy)
                goods = goods.where(Goods.category.in_(ids))
            except Exception as e:
                pass
        start = 0
        per_page_nums = 10
        if request.pagePerNums:
            per_page_nums = request.pagePerNums
        if request.pages:
            start = per_page_nums * (request.pages - 1)
        goods = goods.limit(per_page_nums).offset(start)
        rsp.total = goods.count()
        for good in goods:
            rsp.goods.append(self.convert_model_to_message(good))
        return rsp

    @logger.catch
    def BatchGetGoods(self, request: goods_pb2.BatchGoodsIdInfo, context):
        """
        批量获得商品
        :param request:
        :param context:
        :return:
        """
        rsp = goods_pb2.GoodsListResponse()

        # print(type(request.id))
        # print(request.id)
        # list转换 重点
        goods = Goods.select().where(Goods.id.in_(list(request.id)))
        rsp.total = goods.count()
        for good in goods:
            rsp.goods.append(self.convert_model_to_message(good))
        return rsp

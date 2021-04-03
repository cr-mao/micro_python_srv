from datetime import datetime

from peewee import *
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from playhouse.mysql_ext import JSONField


# 连接池
# ReconnectMixin 防止连接断开
class ReconnectMysqlDATABASE(ReconnectMixin, PooledMySQLDatabase):
    pass


DB = ReconnectMysqlDATABASE("micro_goods_srv", host="127.0.0.1", port=3306, password="", user="root")


class BaseModel(Model):
    class Meta:
        database = DB

    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_deleted = BooleanField(default=False)
    update_time = DateTimeField(default=datetime.now, verbose_name="添加时间")

    def save(self, *args, **kwargs):
        # 新数据
        if self._pk is not None:
            self.update_time = datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def delete(cls, permanently=False):
        if permanently:
            return super().delete()
        else:
            return super().update(is_deleted=True)

    def delete_instance(self, permanently=True, recursive=False, delete_nullable=False):
        if permanently:
            return self.delete(permanently).where(self._pk_expr()).execute()
        else:
            self.is_deleted = True
            self.save()

    @classmethod
    def select(cls, *fields):
        return super().select(*fields).where(cls.is_deleted == False)


class Category(BaseModel):
    name = CharField(max_length=20, verbose_name="名称")
    parent_category = ForeignKeyField("self", verbose_name="父类别", null=True)
    level = IntegerField(default=1, verbose_name="级别")
    is_tab = BooleanField(default=False, verbose_name="是否显示在tab")


class Brands(BaseModel):
    name = CharField(max_length=50, verbose_name="名称", index=True, unique=True)
    logo = CharField(max_length=200, null=True, verbose_name="图标", default="")


class Goods(BaseModel):
    category = ForeignKeyField(Category, verbose_name="商品分类", on_delete='CASCADE')
    brand = ForeignKeyField(Brands, verbose_name="品牌", on_delete='CASCADE')
    on_sale = BooleanField(default=True, verbose_name="是否上架")
    goods_sn = CharField(max_length=50, default="", verbose_name="商品唯一货号")
    name = CharField(max_length=100, verbose_name="商品名称")
    click_num = IntegerField(default=0, verbose_name="点击数")
    sold_num = IntegerField(default=0, verbose_name="商品销售量")
    fav_num = IntegerField(default=0, verbose_name="收藏数")
    market_price = FloatField(default=0, verbose_name="市场价格")
    shop_price = FloatField(default=0, verbose_name="本店价格")
    ship_free = BooleanField(default=True, verbose_name="是否承担运费")
    images = JSONField(verbose_name="商品轮播图")
    desc_images = JSONField(verbose_name="商品详情图")
    goods_front_image = CharField(max_length=200, verbose_name="封面图")
    is_new = BooleanField(default=False, verbose_name="是否新品")
    is_hot = BooleanField(default=False, verbose_name="是否热销")


class GoodsCategoryBrand(BaseModel):
    id = AutoField(primary_key=True, verbose_name="id")
    category = ForeignKeyField(Category, verbose_name="类别")
    brand = ForeignKeyField(Brands, verbose_name="品牌")

    class Meta:
        indexes = (
            (("category", "brand"), True)
        )


class Banner(BaseModel):
    images = CharField(max_length=200, default="", verbose_name="图片url")
    url = CharField(max_length=200, default="", verbose_name="访问url")
    index = IntegerField(default=0, verbose_name="轮播顺序")


if __name__ == "__main__":
    DB.create_tables([Category, Goods, Brands, GoodsCategoryBrand, Banner])

# DB.create_tables([Category])
# c1 = Category(name="crmao1", level=1)
# c2 = Category(name="crmao2", level=1)
# c1.save()
# c2.save()

# c1 = Category.get(Category.id == 1)
# c1.delete_instance(True)

# Category.delete(permanently=True).where(Category.id == 2).execute()

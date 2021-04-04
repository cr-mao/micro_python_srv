from datetime import datetime

from peewee import *
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

# 连接池
# ReconnectMixin 防止连接断开
from inventory_srv.settings import settings


class ReconnectMysqlDATABASE(ReconnectMixin, PooledMySQLDatabase):
    pass


DB = settings.DB


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


class Inventory(BaseModel):
    # 简化逻辑
    goods = IntegerField(verbose_name="商品id", unique=True)
    stocks = IntegerField(verbose_name="库存数", default=0)
    version = IntegerField(verbose_name="版本号", default=0)  # 乐观锁


if __name__ == "__main__":
    DB.create_tables([Inventory])

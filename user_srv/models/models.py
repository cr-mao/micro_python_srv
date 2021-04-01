from peewee import *
from user_srv.settings import settings


class BaseModel(Model):
    class Meta:
        database = settings.DB


class User(BaseModel):
    # 用户模型
    ROLE_CHOICES = (
        (1, "普通用户"),
        (2, "管理员")
    )
    mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号码")
    password = CharField(max_length=100, verbose_name="密码")
    nick_name = CharField(max_length=20, null=True, verbose_name="昵称")
    head_url = CharField(max_length=200, null=True, verbose_name="头像")
    birthday = DateField(null=True, verbose_name="生日")
    address = CharField(max_length=200, null=True, verbose_name="地址")
    desc = TextField(null=True, verbose_name="个人简介")
    role = IntegerField(default=1, choices=ROLE_CHOICES, verbose_name="用户角色")


if __name__ == "__main__":

    # 第一步 生成表
    settings.DB.create_tables([User])
    # 第二步 生成数据 start
    # from passlib.hash import pbkdf2_sha256
    # for i  in range(10):
    #     user = User()
    #     user.nick_name = f"crmao{i}"
    #     user.mobile = f"1875832795{i}"
    #     user.password = pbkdf2_sha256.hash("admin123")
    #     user.save()
    # 第二步 生成数据 end





    # for user in User.select():
    #     print(pbkdf2_sha256.verify("admin123",user.password))
    # import hashlib
    # m = hashlib.md5()
    # m.update(b"123456")
    # print(m.hexdigest())


    # users = User.select().limit(2).offset(0)


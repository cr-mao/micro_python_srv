import time
from datetime import date

import grpc
from loguru import logger
from peewee import DoesNotExist

from user_srv.models.models import User
from user_srv.proto import user_pb2, user_pb2_grpc
from passlib.hash import pbkdf2_sha256
from google.protobuf.empty_pb2 import Empty


class UserServicer(user_pb2_grpc.UserServicer):

    def convert_user_rsp(self, user):
        """
         user 转换成 UserInfoResponse
        """
        user_info_rsp = user_pb2.UserInfoResponse()
        user_info_rsp.id = user.id
        user_info_rsp.passWord = user.password
        user_info_rsp.mobile = user.mobile
        user_info_rsp.role = str(user.role)
        if user.nick_name:
            user_info_rsp.nickName = user.nick_name
        if user.birthday:
            user_info_rsp.birthDay = int(time.mktime(user.birthday.timetuple()))

        return user_info_rsp

    @logger.catch
    def GetUserList(self, request, context):
        rsp = user_pb2.UserListResponse()
        users = User.select()
        rsp.total = users.count()
        per_page_nums = 10
        page = 1
        start = 0
        if request.pSize:
            per_page_nums = request.pSize
        if request.pn:
            start = per_page_nums * (page - 1)
        users = users.limit(per_page_nums).offset(start)
        for user in users:
            rsp.data.append(self.convert_user_rsp(user))

        return rsp

    @logger.catch
    def GetUserById(self, request: user_pb2.IdRequest, context):
        try:
            user = User.get(User.id == request.id)
            user_info_rsp = self.convert_user_rsp(user)
            return user_info_rsp
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse

    @logger.catch
    def CreateUser(self, request, context):
        try:
            user = User.get(User.mobile == request.mobile)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("用户已经存在")
        except DoesNotExist as e:
            pass
        user = User()
        user.nick_name = request.nickName
        user.mobile = request.mobile
        user.password = pbkdf2_sha256.hash(request.passWord)
        user.save()
        return self.convert_user_rsp(user)

    @logger.catch
    def UpdateUser(self, request, context):
        try:
            user = User.get(User.id == request.id)
            user.nick_name = request.nickName
            user.birthday = date.fromtimestamp(request.birthDay)
            user.save()
            return Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse

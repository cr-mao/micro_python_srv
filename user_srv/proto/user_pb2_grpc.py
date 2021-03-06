# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import user_pb2 as user__pb2


class UserStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetUserList = channel.unary_unary(
        '/User/GetUserList',
        request_serializer=user__pb2.PageInfo.SerializeToString,
        response_deserializer=user__pb2.UserListResponse.FromString,
        )
    self.GetUserByMobile = channel.unary_unary(
        '/User/GetUserByMobile',
        request_serializer=user__pb2.MobileRequest.SerializeToString,
        response_deserializer=user__pb2.UserInfoResponse.FromString,
        )
    self.GetUserById = channel.unary_unary(
        '/User/GetUserById',
        request_serializer=user__pb2.IdRequest.SerializeToString,
        response_deserializer=user__pb2.UserInfoResponse.FromString,
        )
    self.CreateUser = channel.unary_unary(
        '/User/CreateUser',
        request_serializer=user__pb2.CreateUserInfo.SerializeToString,
        response_deserializer=user__pb2.UserInfoResponse.FromString,
        )
    self.UpdateUser = channel.unary_unary(
        '/User/UpdateUser',
        request_serializer=user__pb2.UpdateUserInfo.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.CheckPassword = channel.unary_unary(
        '/User/CheckPassword',
        request_serializer=user__pb2.PasswrodCheckInfo.SerializeToString,
        response_deserializer=user__pb2.CheckPasswordResponse.FromString,
        )


class UserServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetUserList(self, request, context):
    """用户列表
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetUserByMobile(self, request, context):
    """mobile 查询用户
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetUserById(self, request, context):
    """通过id 查询用户
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CreateUser(self, request, context):
    """添加用户
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateUser(self, request, context):
    """更新用户 更新失败了呢，  应该统一个code 码 表示成功与否先，暂时先这样
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CheckPassword(self, request, context):
    """检测密码
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_UserServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetUserList': grpc.unary_unary_rpc_method_handler(
          servicer.GetUserList,
          request_deserializer=user__pb2.PageInfo.FromString,
          response_serializer=user__pb2.UserListResponse.SerializeToString,
      ),
      'GetUserByMobile': grpc.unary_unary_rpc_method_handler(
          servicer.GetUserByMobile,
          request_deserializer=user__pb2.MobileRequest.FromString,
          response_serializer=user__pb2.UserInfoResponse.SerializeToString,
      ),
      'GetUserById': grpc.unary_unary_rpc_method_handler(
          servicer.GetUserById,
          request_deserializer=user__pb2.IdRequest.FromString,
          response_serializer=user__pb2.UserInfoResponse.SerializeToString,
      ),
      'CreateUser': grpc.unary_unary_rpc_method_handler(
          servicer.CreateUser,
          request_deserializer=user__pb2.CreateUserInfo.FromString,
          response_serializer=user__pb2.UserInfoResponse.SerializeToString,
      ),
      'UpdateUser': grpc.unary_unary_rpc_method_handler(
          servicer.UpdateUser,
          request_deserializer=user__pb2.UpdateUserInfo.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'CheckPassword': grpc.unary_unary_rpc_method_handler(
          servicer.CheckPassword,
          request_deserializer=user__pb2.PasswrodCheckInfo.FromString,
          response_serializer=user__pb2.CheckPasswordResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'User', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

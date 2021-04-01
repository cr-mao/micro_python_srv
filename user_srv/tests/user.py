import grpc

from user_srv.proto import user_pb2_grpc, user_pb2


class UserTest:
    def __init__(self):
        channel = grpc.insecure_channel("127.0.0.1:50052")
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        rsp: user_pb2.UserInfoResponse = self.stub.GetUserList(user_pb2.PageInfo(pn=2, pSize=2))
        print(rsp.total)

        for user in rsp.data:
            print(user.mobile, user.birthDay)

    def get_user_by_id(self, user_id):
        rsp: user_pb2.UserInfoResponse = self.stub.GetUserById(user_pb2.IdRequest(id=user_id))
        print(rsp)

    def create_user(self, nick_name, mobile, password):
        rsp: user_pb2.UserInfoResponse = self.stub.CreateUser(user_pb2.CreateUserInfo(
            nickName=nick_name,
            passWord=password,
            mobile=mobile
        ))
        print(rsp.id)


if __name__ == "__main__":
    user = UserTest()
    user.user_list()
    # user.get_user_by_id(1)
    # user.create_user("crmao", "18758327999", "123123")

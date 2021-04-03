from loguru import logger

from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc


class InventoryServicer(inventory_pb2_grpc.InventoryServicer):
    pass

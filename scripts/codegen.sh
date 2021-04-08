rm -f user_srv/proto/*pb2.py
rm -f user_srv/proto/*pb2_grpc.py
rm -f goods_srv/proto/*pb2.py
rm -f goods_srv/proto/*pb2_grpc.py
rm -f order_srv/proto/*pb2.py
rm -f order_srv/proto/*pb2_grpc.py

rm -f inventory_srv/proto/*pb2.py
rm -f inventory_srv/proto/*pb2_grpc.py


python -m grpc_tools.protoc -I ./user_srv/proto --python_out=./user_srv/proto --grpc_python_out=./user_srv/proto ./user_srv/proto/user.proto
python -m grpc_tools.protoc -I ./goods_srv/proto --python_out=./goods_srv/proto --grpc_python_out=./goods_srv/proto ./goods_srv/proto/goods.proto
python -m grpc_tools.protoc -I ./inventory_srv/proto --python_out=./inventory_srv/proto --grpc_python_out=./inventory_srv/proto ./inventory_srv/proto/inventory.proto

# 订单相关
python -m grpc_tools.protoc -I ./order_srv/proto --python_out=./order_srv/proto --grpc_python_out=./order_srv/proto ./order_srv/proto/order.proto
python -m grpc_tools.protoc -I ./order_srv/proto --python_out=./order_srv/proto --grpc_python_out=./order_srv/proto ./order_srv/proto/goods.proto
python -m grpc_tools.protoc -I ./order_srv/proto --python_out=./order_srv/proto --grpc_python_out=./order_srv/proto ./order_srv/proto/inventory.proto

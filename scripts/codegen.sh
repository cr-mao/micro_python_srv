rm -f user_srv/proto/*.py
rm -f goods_srv/proto/*.py
rm -f inventory_srv/proto/*.py
python -m grpc_tools.protoc -I ./user_srv/proto --python_out=./user_srv/proto --grpc_python_out=./user_srv/proto ./user_srv/proto/user.proto
python -m grpc_tools.protoc -I ./goods_srv/proto --python_out=./goods_srv/proto --grpc_python_out=./goods_srv/proto ./goods_srv/proto/goods.proto
python -m grpc_tools.protoc -I ./inventory_srv/proto --python_out=./inventory_srv/proto --grpc_python_out=./inventory_srv/proto ./inventory_srv/proto/inventory.proto

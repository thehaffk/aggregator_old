include .env
export

 .PHONY: run-service
run-service:
	poetry run python3.11 homepp

 .PHONY: generate-proto
generate-proto:
	poetry run python3.11 -m grpc_tools.protoc \
	-I homepp/infrastructure/rpc/proto \
	--python_out=homepp/infrastructure/rpc/generated \
	--pyi_out=homepp/infrastructure/rpc/generated \
	--grpc_python_out=homepp/infrastructure/rpc/generated \
	homepp/infrastructure/rpc/proto/$(path)
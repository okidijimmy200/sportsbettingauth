# User management service

A user management service that makes use of the Hexagonal Architectural Pattern.

## Generating protobuf files

The protobuf files are generated using the protoc compiler. The compiler is available for download [here]()

```shell
python -m grpc_tools.protoc -I./protos protos/auth.proto --python_out=. --grpc_python_out=./generated
```

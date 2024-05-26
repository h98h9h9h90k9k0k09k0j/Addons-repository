#!/bin/bash

# Activate the virtual environment
source /opt/venv/bin/activate
echo "activated virtual environment"

# Generate the gRPC code from the protobuf definitions
python -m grpc_tools.protoc -I/app/server --python_out=/app/server --grpc_python_out=/app/server /app/server/workloads.proto
echo "generated protobuf files"

# Start the main application
echo "starting the server"
python /app/server/main.py

# Wait for any process to edocker run -it --entrypoint /bin/sh aleksanderrdl/hass-distribute-addon:server_alpine_aarch64
echo "waiting for process to exit"
wait -n

# Exit with status of process that exited first
echo "exiting"
exit $?
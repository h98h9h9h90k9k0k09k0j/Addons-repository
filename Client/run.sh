#!/bin/bash

# Activate the virtual environment
source /opt/venv/bin/activate
echo "activated virtual environment"

# Generate the gRPC code from the protobuf definitions
python -m grpc_tools.protoc -I/app/client --python_out=/app/client --grpc_python_out=/app/client /app/client/workloads.proto
echo "generated protobuf files"

# Start the main application
echo "starting the client"
python /app/client/main.py

# Wait for any process to exit
echo "waiting for process to exit"
wait -n

# Exit with status of process that exited first
echo "exiting"
exit $?
#!/bin/bash

# Start nginx with debug options
nginx -g "daemon off;error_log /dev/stdout debug;" &

# Run the custom startup script
bash run.sh
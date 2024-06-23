#!/bin/bash

# Start nginx with debug options
nginx -c /usr/share/nginx/html/nginx.conf -g "daemon off;" &
echo "IM RUNNING"

# Run the custom startup script
bash run.sh
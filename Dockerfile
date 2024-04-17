FROM alpine:3.19

# Install requirements for add-on
RUN apk add --no-cache \
    python3 \
    py3-pip \
  && pip3 install --no-cache-dir \
    pyyaml==5.4.1 \
    websockets==12.0
        
# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Copy data for add-on
COPY addon.py /
COPY config.yaml /

# Set working directory
WORKDIR /

# Start the addon
CMD ["python3", "-u", "addon.py" ] 
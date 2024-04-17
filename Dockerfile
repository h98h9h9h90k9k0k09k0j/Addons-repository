# Downloaded from https://github.com/home-assistant/docker-base example: ghcr.io/home-assistant/amd64-base which is alpine:3.19 https://hub.docker.com/layers/amd64/alpine/3.19/images/sha256-6457d53fb065d6f250e1504b9bc42d5b6c65941d57532c072d929dd0628977d0?context=explore
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

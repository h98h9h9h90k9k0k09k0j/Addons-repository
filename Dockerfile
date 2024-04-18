# Downloaded from https://github.com/home-assistant/docker-base example: ghcr.io/home-assistant/amd64-base which is alpine:3.19 https://hub.docker.com/layers/amd64/alpine/3.19/images/sha256-6457d53fb065d6f250e1504b9bc42d5b6c65941d57532c072d929dd0628977d0?context=explore
FROM alpine:3.19

# Install Python, pip and necessary build dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip 
    #python3-dev \   The outcommented dependencies might become necessary depending on what we need later but idk
    #gcc \         
    #musl-dev  \       
    #libffi-dev \     
    #openssl-dev 

# Create a virtual environment in the /opt/venv directory
RUN python3 -m venv /opt/venv

# Set the environment variable to ensure commands and scripts run in the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages in the virtual environment
RUN pip install --no-cache-dir pyyaml websockets
        

# Set shell
SHELL ["/bin/sh", "-o", "pipefail", "-c"]

# Copy data for add-on
COPY addon.py /
COPY config.yaml /
# Set working directory
WORKDIR /

# Start the addon
CMD ["python3", "-u", "addon.py" ] 

COPY rootfs /
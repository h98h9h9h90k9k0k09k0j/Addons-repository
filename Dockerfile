# Downloaded from https://github.com/home-assistant/docker-base example: ghcr.io/home-assistant/amd64-base which is alpine:3.19 https://hub.docker.com/layers/amd64/alpine/3.19/images/sha256-6457d53fb065d6f250e1504b9bc42d5b6c65941d57532c072d929dd0628977d0?context=explore
FROM alpine:3.19

# Install Python, pip and necessary build dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \ 
    gcc \       
    g++ \  
    musl-dev  \       
    libffi-dev \    
    openblas-dev \  
    lapack-dev \    
    cmake \          
    openssl-dev \
    # alpine package for opencv
    opencv-dev  \ 
    bash

# Set working directory
WORKDIR /app

# Copy data for add-on
COPY . /app

# Create a virtual environment in the /opt/venv directory
RUN python3 -m venv /opt/venv \
    && source /opt/venv/bin/activate 

# Set the environment variable to ensure commands and scripts run in the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages in the virtual environment
RUN pip install --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt
        
RUN chmod +x /app/run.sh

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

EXPOSE 3030 8000

# Start the addon
CMD ["bash", "run.sh" ] 

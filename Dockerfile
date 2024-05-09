# Home Assistant Debian base image
FROM ghcr.io/home-assistant/amd64-base-debian:bookworm

# Install Python and necessary build dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libopencv-dev \
    python3.11-venv \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy data for add-on
COPY . /app

# Create a virtual environment in the /opt/venv directory
RUN python3 -m venv /opt/venv \
    && . /opt/venv/bin/activate 

# Set the environment variable to ensure commands and scripts run in the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages in the virtual environment
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Ensure the main script is executable
RUN chmod +x /app/run.sh

# Use bash for running commands
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Expose necessary ports
EXPOSE 3030 8000

# Command to run the Home Assistant add-on
CMD ["bash", "run.sh"]

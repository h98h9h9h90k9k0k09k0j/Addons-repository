# Hvad bruger jeg dem her til?
ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN apk add --no-cache \
    python3 \
    py3-pip \
  && pip3 install --no-cache-dir \
    pyyaml \
    websockets
    
# Copy data for add-on
COPY addon.py /
COPY config.yaml /

# Set working directory
WORKDIR /

# Start the addon
CMD ["python3", "-u", "addon.py" ] 
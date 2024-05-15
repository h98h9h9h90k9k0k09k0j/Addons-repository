ARG BUILD_FROM
FROM $BUILD_FROM

#FROM aleksanderrdl/hass-distribute-addon:server_alpine_aarch64

# Execute during the build of the image
ARG TEMPIO_VERSION BUILD_ARCH
RUN \
    curl -sSLf -o /usr/bin/tempio \
    "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

# copy run file
COPY . /app

# Convert any scripts that might have Windows line endings to Unix line endings
RUN dos2unix /app/run.sh

# Ensure the main script is executable
RUN chmod a+x /app/run.sh

# Command to run the Home Assistant add-on
CMD ["bash", "run.sh"]
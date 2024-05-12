#ARG BUILD_FROM
#FROM $BUILD_FROM
FROM aleksanderrdl/hass-distribute-addon:server_amd64

# copy run file
COPY run.sh /app
COPY config.yaml /app

# Convert any scripts that might have Windows line endings to Unix line endings
RUN dos2unix /app/run.sh

# Ensure the main script is executable
RUN chmod a+x /app/run.sh

# Command to run the Home Assistant add-on
CMD ["bash", "run.sh"]
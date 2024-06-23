ARG BUILD_FROM
FROM $BUILD_FROM

# Execute during the build of the image
ARG TEMPIO_VERSION BUILD_ARCH
RUN \
    curl -sSLf -o /usr/bin/tempio \
    "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

RUN apt-get update && apt-get install -y \
    nginx dos2unix

# Copy the nginx configuration file
COPY www/nginx.conf /etc/nginx/conf.d/default.conf

# Copy WebUI files
COPY www /usr/share/nginx/html

# copy run file
COPY run.sh /run.sh
COPY entrypoint.sh /entrypoint.sh

# Convert any scripts that might have Windows line endings to Unix line endings
RUN dos2unix /run.sh
RUN dos2unix /entrypoint.sh

# Ensure the main script is executable
RUN chmod a+x /run.sh
RUN chmod a+x /entrypoint.sh

# Command to run the Home Assistant add-on
CMD ["/entrypoint.sh"]
ARG BUILD_FROM
FROM $BUILD_FROM

# Execute during the build of the image
ARG TEMPIO_VERSION BUILD_ARCH
RUN \
    curl -sSLf -o /usr/bin/tempio \
    "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

RUN apt-get update && apt-get install -y \
    nginx \
    \
    && mkdir -p /run/nginx

#Copy our conf into the nginx http.d folder.
COPY ingress.conf /etc/nginx/http.d/
# Copy WebUI files
COPY Frontend /usr/share/nginx/html
# copy run file
COPY . /app

# Convert any scripts that might have Windows line endings to Unix line endings
RUN dos2unix /app/run.sh
RUN dos2unix /app/entrypoint.sh

# Ensure the main script is executable
RUN chmod a+x /app/run.sh
RUN chmod a+x /app/entrypoint.sh

# Command to run the Home Assistant add-on
CMD ["bash", "entrypoint.sh"]
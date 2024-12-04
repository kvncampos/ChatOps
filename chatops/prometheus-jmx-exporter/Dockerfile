FROM openjdk:8-jdk

# Create directory for JMX Prometheus HTTP server
RUN mkdir -p /opt/jmx_prometheus_httpserver && \
    wget 'https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_httpserver/0.16.1/jmx_prometheus_httpserver-0.16.1-jar-with-dependencies.jar' \
        -O /opt/jmx_prometheus_httpserver/jmx_prometheus_httpserver.jar

# Download and set up confd
ADD https://github.com/kelseyhightower/confd/releases/download/v0.11.0/confd-0.11.0-linux-amd64 /usr/local/bin/confd
RUN chmod +x /usr/local/bin/confd

# Ensure confd directory exists and copy configuration
COPY confd /etc/confd/

# Copy entrypoint script
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/opt/entrypoint.sh"]

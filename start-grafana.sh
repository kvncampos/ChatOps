FROM grafana/grafana:latest

# Copy the startup script into the container
COPY start-grafana.sh /start-grafana.sh
RUN chmod +x /start-grafana.sh

# Use the script as the entrypoint
ENTRYPOINT ["/bin/bash", "/start-grafana.sh"]

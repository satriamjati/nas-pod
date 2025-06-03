FROM docker.io/servercontainers/samba

# Install Python and Flask dependencies
RUN apk add --no-cache python3 py3-pip py3-flask samba

# Create and set up the virtual environment
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install flask waitress

# Copy your Flask app and run.py script into the container
COPY api.py /api.py
COPY run.py /run.py

# Copy the entrypoint script to start both services
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint to run the script that starts both services
ENTRYPOINT ["/entrypoint.sh"]

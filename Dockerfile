FROM selenium/standalone-chrome:4.27.0-20241225

# Switch to root user for privileged operations
USER root

# Fix permissions and setup
RUN rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/lib/apt/lists/partial && \
    chmod -R 755 /var/lib/apt/lists && \
    sed -i '/^deb.*main.*$/!b;n;d' /etc/apt/sources.list

# Install Python, pip, and venv
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean

# Create the working directory and fix permissions
WORKDIR /app
RUN mkdir -p /app && chown seluser:seluser /app

# Switch to seluser
USER seluser

# Copy application files
COPY selenium_test.py /app/
COPY requirements.txt /app/

# Create a virtual environment and install dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Run the application using the virtual environment
CMD ["/app/venv/bin/python", "selenium_test.py"]


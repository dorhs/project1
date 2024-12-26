# Base image with Python and Chrome
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install selenium

# Set environment variables
ENV DISPLAY=:99

# Copy script into the container
COPY selenium.py /app/selenium.py

# Set the working directory
WORKDIR /app

# Command to run the Selenium script
CMD ["python", "selenium_script.py"]

# Base image with Python
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy Python script and requirements file into the container
COPY selenium_test.py /app/selenium_test.py
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install necessary tools and Chrome dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Check if URL is correct and download the Chrome package
RUN wget -q --spider https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.198-1_amd64.deb || \
    (echo "Download failed, trying alternative URL." && \
    wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_113.0.5672.63-1_amd64.deb)

# Install Google Chrome
RUN apt-get update && apt-get install -y ./google-chrome-stable_114.0.5735.198-1_amd64.deb && \
    rm google-chrome-stable_114.0.5735.198-1_amd64.deb || \
    (echo "Chrome installation failed" && exit 1)

# Install ChromeDriver for the specific Chrome version
RUN wget -q "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Ensure ChromeDriver is in PATH
ENV PATH="/usr/local/bin:${PATH}"

# Command to run the Selenium script
CMD ["python", "selenium_test.py"]

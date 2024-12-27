# Base image with Python
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your Python script and dependencies
COPY selenium_test.py .
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install necessary tools and Chrome
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip curl gnupg && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    wget -q "https://chromedriver.storage.googleapis.com/116.0.5845.96/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && mv chromedriver /usr/local/bin/chromedriver && chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add ChromeDriver to PATH
ENV PATH="/usr/local/bin:${PATH}"

# Run Selenium script
CMD ["python", "selenium_test.py"]

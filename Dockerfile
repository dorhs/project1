# Base image with Python and Chrome
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy Python script and requirements file into the container
COPY selenium_test.py /app/selenium_test.py
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install Chrome and necessary dependencies
RUN apt-get update && apt-get install -y wget unzip curl && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# Install ChromeDriver for the installed Chrome version
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f1-3) && \
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}") && \
    if [ -z "$CHROMEDRIVER_VERSION" ]; then \
        echo "Failed to fetch ChromeDriver version for Chrome version $CHROME_VERSION"; exit 1; \
    fi && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Command to run the Selenium script
CMD ["python", "selenium_test.py"]

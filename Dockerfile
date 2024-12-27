# Base image with Python and Chrome
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy Python script and requirements file into the container
COPY selenium_test.py /app/selenium_test.py
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install a specific version of Chrome and necessary dependencies
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.198-1_amd64.deb && \
    apt install -y ./google-chrome-stable_114.0.5735.198-1_amd64.deb && \
    rm google-chrome-stable_114.0.5735.198-1_amd64.deb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Command to run the Selenium script
CMD ["python", "selenium_test.py"]

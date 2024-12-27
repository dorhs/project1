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
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# Command to run the Selenium script
CMD ["python", "selenium_test.py"]

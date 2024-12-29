# Use the Selenium standalone Chrome image as the base image
FROM selenium/standalone-chrome:4.27.0-20241225

# Set the working directory inside the container
WORKDIR /app

# Copy your Python script and requirements file into the container
COPY selenium_test.py /app/
#COPY requirements.txt /app/

# Install any additional Python dependencies if required
#RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run your Selenium script
CMD ["python", "selenium_test.py"]

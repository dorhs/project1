FROM python
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver
RUN mkdir /selenium_test
RUN chmod 777 /selenium_test
COPY . /selenium_test
WORKDIR /selenium_test
RUN pip install -r requirements.txt
CMD ["python", "selenium_test.py"]

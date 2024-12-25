FROM python
RUN mkdir /tpp
RUN chmod 777 /tpp
COPY . /tpp
WORKDIR /tpp
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

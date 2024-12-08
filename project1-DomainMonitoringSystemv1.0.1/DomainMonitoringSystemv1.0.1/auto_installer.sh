#!/bin/bash
# install Docker and create image
git clone -b DomainMonitoringSystemv1.0.1 https://github.com/Idayan88/project1.git
echo "The clone op Done"
sudo apt update -y
sudo apt install docker.io -y
cd /home/ubuntu/project1/DomainMonitoringSystemv1.0.1
cat << EOF > "Dockerfile"
FROM python 
RUN mkdir /tpp
RUN chmod 777 /tpp
COPY . /tpp
WORKDIR /tpp
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
EOF
sudo docker pull python
sudo docker build -t tpp:1.0.0 .
sudo docker run -d -p 8080:8080 --name tpp-app tpp:1.0.0

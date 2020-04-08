FROM ubuntu:latest

# Set the home dir to /app and move into it
ENV HOME /app
WORKDIR /app

# install python-pip and python-dev on ubuntu
RUN apt-get update && apt-get install -y python3-pip python3-dev default-libmysqlclient-dev

RUN apt-get install -y python3-pip python3-dev

#copy everything from the current directory into the image /app dir
COPY . .


RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

# Allow port 8000 to be accessed
EXPOSE 8000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait


CMD  /wait && python3 run.py
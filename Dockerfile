FROM ubuntu:latest

RUN apt-get update

# Set the home dir to /app and move into it
ENV HOME /app
WORKDIR /app

# install python-pip and python-dev on ubuntu
RUN apt-get install -y python-pip python-dev

RUN apt-get install -y python3-pip python3-dev

#copy everything from the current directory into the image /app dir
COPY . .

RUN pip install -r requirements.txt
RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

# Allow port 8000 to be accessed
EXPOSE 8000

ENTRYPOINT [ "python" ]
ENTRYPOINT [ "python3" ]

CMD [ "run.py" ]
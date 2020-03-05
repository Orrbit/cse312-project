FROM ubuntu:latest

RUN apt-get update

# Set the home dir to /app and move into it
ENV HOME /app
WORKDIR /app

# install python-pip and python-dev on ubuntu
RUN apt-get install -y python-pip python-dev

#copy everything from the current directory into the image /app dir
COPY . .

RUN pip install -r requirements.txt

# Allow port 8000 to be accessed
EXPOSE 8000

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]
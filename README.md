To get the server up, build an image using:

docker build -t biazza-image:latest

And then run an instance of that image using

docker run -d -p 8000:8000 biazza-image:latest

Verify that the image is running with port 8000 open using 

docker ps -a

Navigate to localhost:8000
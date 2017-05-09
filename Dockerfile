FROM resin/edison-python:latest
# Enable systemd
ENV INITSYSTEM on

#Copy contents of app from our repo into /usr/src/app into our container.
ADD app/ /usr/src/app

# OpenCV
RUN apt-get update
RUN apt-get install -y python python-dev python-pip python-pygame libraspberrypi-bin

RUN apt-get install libopencv-dev python-opencv

#run hello.py when the container starts on the device.
CMD ["python", "usr/src/app/hello.py"]

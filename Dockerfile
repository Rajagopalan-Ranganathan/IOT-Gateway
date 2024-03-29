FROM resin/intel-edison-python:latest
# Enable systemd
ENV INITSYSTEM on


RUN pip install opencv-python python-firebase
#Copy contents of app from our repo into /usr/src/app into our container.
ADD app/ /usr/src/app

#run hello.py when the container starts on the device.
CMD ["python", "usr/src/app/head-count.py"]

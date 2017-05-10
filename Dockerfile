FROM pcarranzav/opencv

RUN apt-get update \
	&& apt-get install -y software-properties-common \
	&& add-apt-repository ppa:mc3man/trusty-media \
	&& apt-get update \
	&& apt-get install -y ffmpeg libxine1

#Copy contents of app from our repo into /usr/src/app into our container.
ADD app/ /usr/src/app

# OpenCV
RUN apt-get update
RUN apt-get install -y python python-dev python-pip python-pygame

RUN apt-get install libopencv-dev python-opencv

#run hello.py when the container starts on the device.
CMD ["python", "usr/src/app/hello.py"]

FROM resin/intel-edison-python:latest
# Enable systemd
ENV INITSYSTEM on

RUN apt-get update \
	&& apt-get install -y -q \
		wget \
		curl \
		build-essential \
		cmake \
		python2.7 \
		python2.7-dev \
		libavformat-dev \
		libavcodec-dev \
		libavfilter-dev \
		libswscale-dev \
		libgtk2.0-dev \
		libjpeg-dev \
		libpng-dev \
		libtiff-dev \
		libjasper-dev \
		zlib1g-dev \
		libopenexr-dev \
		libeigen3-dev \
		libtbb-dev \
		pkg-config \
		xserver-xorg-core \
		xorg \
		libgtk2.0-0 \
		unzip


RUN pip install opencv-python
#Copy contents of app from our repo into /usr/src/app into our container.
ADD app/ /usr/src/app

#run hello.py when the container starts on the device.
CMD ["python", "usr/src/app/hello.py"]

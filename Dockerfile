FROM resin/edison-python:latest
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

RUN wget 'https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg' \
  	&& /bin/sh setuptools-0.6c11-py2.7.egg \
  	&& rm -f setuptools-0.6c11-py2.7.egg
RUN curl 'https://bootstrap.pypa.io/get-pip.py' | python2.7
RUN pip install numpy


COPY scripts/ /usr/src/scripts

RUN /bin/sh  /usr/src/scripts/build_opencv.sh

RUN apt-get update \
		&& apt-get install -y software-properties-common \
		&& add-apt-repository ppa:mc3man/trusty-media \
		&& apt-get update \
		&& apt-get install -y ffmpeg libxine1

#Copy contents of app from our repo into /usr/src/app into our container.
ADD app/ /usr/src/app

#run hello.py when the container starts on the device.
CMD ["python", "usr/src/app/hello.py"]

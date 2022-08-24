# The distribution for this container is based on the following:
FROM ubuntu:latest

USER root

# Update the package index
RUN apt update -y && apt upgrade -y
RUN apt install -y software-properties-common gcc && \
	add-apt-repository -y ppa:deadsnakes/ppa && \
	add-apt-repository ppa:mozillateam/ppa
ARG DEBIAN_FRONTEND=noninteractive
RUN apt install -y python3 python3-pip python3-distutils python3-apt
RUN apt install -y --no-install-recommends \
	ca-certificates curl firefox-esr wget
RUN rm -fr /var/lib/apt/lists/*

# Download and install geckodriver
RUN curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin

# install firefox
RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
	wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
	tar xjf $FIREFOX_SETUP -C /opt/ && \
	ln -s /opt/firefox/firefox /usr/bin/firefox && \
	rm $FIREFOX_SETUP

# Download and install the latest version of pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
RUN python3 /tmp/get-pip.py
RUN apt purge -y ca-certificates curl wget

# Add the user and group
#RUN useradd -ms /bin/sh user
#USER user

# Install the requirements for the application
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

# Open a terminal
CMD ["/bin/sh"]

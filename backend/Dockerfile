FROM ubuntu:16.04

RUN apt-get install -y \
    apt-utils \
    python-pip \
    python-software-properties 

ADD ./requirements.txt /tmp/

RUN pip3 install --upgrade pip

RUN pip3 install -r /tmp/requirements.txt

EXPOSE 8000

WORKDIR /root/messenger


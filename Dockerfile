FROM python:3.7-buster

RUN apt-get update && \
    DEBIAN_FRONTEND=non-interactive apt-get -y install \
            build-essential \
            python3-dev 

RUN apt-get update && \
    DEBIAN_FRONTEND=non-interactive apt-get -y install  \
            libsodium23                                 \
            python3-nacl

RUN pip3 install pytest requests responses 

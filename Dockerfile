FROM python:3.7-buster

RUN apt-get update && \
    DEBIAN_FRONTEND=non-interactive apt-get -y install \
            build-essential \
            python3-dev 

RUN apt-get update && \
    DEBIAN_FRONTEND=non-interactive apt-get -y install  \
            libsodium23                                 \
            python3-nacl

ENV PYTHONUNBUFFERED=1
WORKDIR /app
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD ["gunicorn", "app:app"]

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
COPY keygen.py /app/keygen.py
RUN chmod a+x /entrypoint.sh
#RUN pip3 install pytest requests responses 

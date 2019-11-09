FROM python:3.7-buster

RUN apt-get update && \
    DEBIAN_FRONTEND=non-interactive apt-get -y install \
            build-essential \
            python3-dev 

RUN apt-get update && \
    DEBIAN_FRONTEND=non-interactive apt-get -y install  \
            libsodium23                                 \
            python3-nacl


ARG GUNICORN_PORT=888
EXPOSE $GUNICORN_PORT
ENV GUNICORN_PORT=$GUNICORN_PORT                             \
    GUNICORN_WORKERS=2                                       \
    GUNICORN_CMD_ARGS="--access-logfile - --error-logfile -" \
    PYTHONUNBUFFERED=1
WORKDIR /app
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD ["gunicorn", "wsid.server:app"]

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

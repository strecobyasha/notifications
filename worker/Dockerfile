FROM python:3.10-slim

WORKDIR /opt
COPY worker/requirements.txt .

RUN  apt-get update

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]

COPY ./worker .
COPY ./broker broker
COPY ./messages messages
COPY ./utils utils

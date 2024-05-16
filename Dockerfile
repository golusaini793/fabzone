FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y \
    curl \
    libxrender1 \
    libfontconfig \
    libxtst6 \
    xz-utils \
    apt-utils \
    gettext


RUN mkdir /fabzone
WORKDIR /fabzone
COPY requirements.txt /fabzone/
RUN pip install -r requirements.txt
COPY . /fabzone//
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh


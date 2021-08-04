FROM python:slim
LABEL maintainer="jon.covington@gmail.com"

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get upgrade
RUN pip install -U pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
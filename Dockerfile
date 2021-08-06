FROM python:slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get upgrade
RUN pip install -U pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# RUN groupadd -r appuser
# RUN useradd -s /bin/bash -g appuser -u 1001 appuser


RUN mkdir /app
RUN mkdir /app/static
WORKDIR /app

ADD entrypoint-prod.sh /entrypoint-prod.sh
# RUN chown appuser:appuser /entrypoint-prod.sh

COPY ./app .

# USER appuser
ENTRYPOINT ["/entrypoint-prod.sh"]
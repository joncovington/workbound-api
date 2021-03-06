FROM python:slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y dos2unix
RUN pip install -U pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# RUN groupadd -r appuser
# RUN useradd -s /bin/bash -g appuser -u 1001 appuser

RUN mkdir /app
RUN mkdir /app/static
WORKDIR /app

ADD entrypoint-prod.sh /entrypoint-prod.sh
RUN chmod a+x /entrypoint-prod.sh

COPY ./app .
EXPOSE 8000
RUN dos2unix /entrypoint-prod.sh
# USER appuser
ENTRYPOINT ["/entrypoint-prod.sh"]
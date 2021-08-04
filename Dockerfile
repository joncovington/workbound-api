###########
# BUILDER #
###########

FROM python:slim
LABEL maintainer="jon.covington@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get upgrade
RUN pip install -U pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

COPY ./app .

#########
# FINAL #
#########

FROM python:slim

RUN mkdir -p /home/app

WORKDIR /home/app

RUN apt-get update
RUN apt-get upgrade

COPY --from=0 /usr/src/app/wheels /wheels
COPY --from=0 /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./app .

ADD entrypoint-prod.sh /entrypoint-prod.sh
RUN chmod a+x /entrypoint-prod.sh
ENTRYPOINT ["/entrypoint-prod.sh"]
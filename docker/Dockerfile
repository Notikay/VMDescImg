# Dockerfile "Сервис расчета по методам Blasingame"


FROM python:3.13.2-slim

WORKDIR /VMDescImg

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/VMDescImg

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY .env .
COPY config.yml .
COPY ./src .

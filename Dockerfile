FROM python:3.7-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY . /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
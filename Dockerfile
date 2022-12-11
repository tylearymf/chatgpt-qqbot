# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV QQ_NUMBER=
ENV CHATGPT_TOKEN=
ENV LISTEN_PORT=8700
ENV POST_PORT=10016

COPY . ./
ENTRYPOINT ["python", "main.py"]

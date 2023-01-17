FROM python:latest

COPY ./src /app/src
WORKDIR /app/src

RUN pip3 install -r /app/src/requirements.txt

EXPOSE 8000
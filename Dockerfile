FROM python:3.10

COPY ./src /app/src
COPY ./requirements/base.txt /app/requirements/base.txt
WORKDIR /app/src

RUN apt-get update && apt-get install -y wkhtmltopdf
RUN pip3 install -r /app/requirements/base.txt

EXPOSE 8000
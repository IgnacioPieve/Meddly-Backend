FROM python:3.10

COPY ./src /app/src

WORKDIR /app/src

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"]
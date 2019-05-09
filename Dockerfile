FROM python:3.5

RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt

COPY ./server.py /app

CMD python server.py

EXPOSE 5000
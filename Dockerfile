FROM python:3.5

COPY ./requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt

COPY ./server.py /app

CMD python server.py

EXPOSE 5000
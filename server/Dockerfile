FROM python:3.5

#VOLUME /app/tmp
RUN mkdir -p /app/tmp
WORKDIR /app/tmp

RUN pip install tensorflow  && pip install bert-serving-server && apt-get update && apt-get install unzip && wget https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip && \\
unzip uncased_L-12_H-768_A-12.zip && rm uncased_L-12_H-768_A-12.zip

RUN mkdir -p /app

CMD bert-serving-start -model_dir /app/tmp/uncased_L-12_H-768_A-12/ -num_worker=1

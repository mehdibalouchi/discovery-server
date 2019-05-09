FROM python:3.6

VOLUME /app/tmp

RUN pip install bert-serving-server && apt-get update && apt-get install unzip && mkdir -p /app/tmp && cd /app/tmp && wget https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip && \\
unzip uncased_L-12_H-768_A-12.zip && rm uncased_L-12_H-768_A-12.zip

CMD bert-serving-start -model_dir /app/tmp/english_L-12_H-768_A-12/ -num_worker=1

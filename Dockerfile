FROM python:3.10

WORKDIR /logistics-real-time-poc
COPY . /logistics-real-time-poc

RUN pip install faker==20.1.0 confluent-kafka==2.3.0

WORKDIR /logistics-real-time-poc/producer
CMD ["python", "main.py"]
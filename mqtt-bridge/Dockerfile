FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir paho-mqtt msgpack cbor2

COPY jsonParser.py .

CMD ["python", "-u", "jsonParser.py"]
FROM python:3.11

COPY / home
COPY src/consumer/requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

ENTRYPOINT ["python", "home/src/consumer/my_consumer.py"]
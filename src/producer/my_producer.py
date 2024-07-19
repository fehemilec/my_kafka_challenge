import logging

from pathlib import Path
from kafka import KafkaProducer
from kafka.errors import KafkaError

import json
from collections import namedtuple


Broker = namedtuple("Broker", ["host", "port", "authentication"])


def get_kafka_producer_client(certs_path, broker: Broker):

    if broker.authentication:
        producer = KafkaProducer(
            bootstrap_servers=[f"{broker.host}:{broker.port}"],
            security_protocol="SSL",
            ssl_check_hostname=False,
            ssl_cafile=f"{certs_path}/server_certs/CARoot.pem",
            ssl_certfile=f"{certs_path}/server_certs/ca-cert",
            ssl_keyfile=f"{certs_path}/server_certs/ca-key",
            ssl_password="fehemi",
            value_serializer=lambda m: json.dumps(m).encode("ascii"),
        )
    else:
        producer = KafkaProducer(
            bootstrap_servers=[f"{broker.host}:{broker.port}"],
            value_serializer=lambda m: json.dumps(m).encode("ascii"),
        )
    return producer


def send_message_json(producer_client, order):

    producer_client.send("orders", order.__dict__)
    logging.info(
        "Sending data package to Broker order: %s %s", order.orderId, order.price
    )
    # Ensure all messages are sent before closing the producer
    producer_client.flush()


def send_message(message, host, port):

    producer = KafkaProducer(bootstrap_servers=[f"{host}:{port}"])
    producer.send("orders", message.encode())
    ## Ensure all messages are sent before closing the producer
    producer.flush()


def get_kafka_broker(broker_id, auth_required):
    brokers = {
        "1": Broker("kafka-1", 9093 if auth_required else 9092, auth_required),
        "2": Broker("localhost", 9095 if auth_required else 9094, auth_required),
        "3": Broker("localhost", 9097 if auth_required else 9096, auth_required),
    }
    return brokers[broker_id]


if __name__ == "__main__":

    # If I send data to a port with ssl enabled,
    # without certificate, I get error
    try:
        abs_path = Path(__file__).parent.parent.parent

        broker = get_kafka_broker(broker_id="1", auth_required=True)
        print("Sending data package to Broker on:", broker.host, broker.port)
        producer_client = get_kafka_producer_client(abs_path, broker)

        send_message_json(
            producer_client=producer_client,
            order={"orderId": "1920", "items": 3, "price": "123.98"},
        )
        print("Message sent")
    except KafkaError as e:
        print("Kafka error: ", e)

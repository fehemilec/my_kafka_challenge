from pathlib import Path
from kafka import KafkaProducer
from kafka.errors import KafkaError

import json
#from utils.models import Broker


def get_kafka_producer_client(host, port, auth_required, certs_path):

    if auth_required:
        producer = KafkaProducer(
            bootstrap_servers=[f"{host}:{port}"],
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
            bootstrap_servers=[f"{host}:{port}"],
            value_serializer=lambda m: json.dumps(m).encode("ascii"),
        )
    return producer


def get_kafka_producer_client2(certs_path, broker):

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
    producer_client.send("users", order)

    # Ensure all messages are sent before closing the producer
    producer_client.flush()


def send_message(message, host, port):

    producer = KafkaProducer(bootstrap_servers=[f"{host}:{port}"])
    producer.send("orders", message.encode())
    ## Ensure all messages are sent before closing the producer
    producer.flush()


if __name__ == "__main__":

    # If I send data to a port with ssl enabled,
    # without certificate, I get error
    try:
        abs_path = Path(__file__).parent.parent.parent

        # broker1_auth = Broker("localhost", "9095", False)
        # producer_client = get_kafka_producer_client2(abs_path, broker1_auth)

        producer_client = get_kafka_producer_client(
            host="localhost", port=9093, auth_required=True, certs_path=abs_path
        )
        send_message_json(
            producer_client=producer_client,
            order={"orderId": "1920", "price": "110.98"},
        )
        print("Message sent")
        # send_message(message="Hi broker 2", host="localhost", port="9094")
    except KafkaError as e:
        print("Kafka error: ", e)

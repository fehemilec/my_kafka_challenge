from pathlib import Path
from kafka.consumer import KafkaConsumer
from kafka.errors import KafkaError


def get_kafka_consumer_client(host, port, certs_path, auth_required=False):

    if auth_required:
        consumer = KafkaConsumer(
            "users",
            bootstrap_servers=[f"{host}:{port}"],
            security_protocol="SSL",
            ssl_check_hostname=False,
            ssl_cafile=f"{certs_path}/server_certs/CARoot.pem",
            ssl_certfile=f"{certs_path}/server_certs/ca-cert",
            ssl_keyfile=f"{certs_path}/server_certs/ca-key",
            ssl_password="fehemi",
        )
    else:
        consumer = KafkaConsumer("users", bootstrap_servers=[f"{host}:{port}"])
    return consumer


if __name__ == "__main__":

    abs_path = Path(__file__).parent.parent.parent

    try:
        consumer = get_kafka_consumer_client(
            host="localhost", port=9093, certs_path=abs_path, auth_required=True
        )

        for message in consumer:
            # decode bytes
            value = message.value.decode("utf-8")
            print(
                "%s:%d:%d: key=%s value=%s"
                % (message.topic, message.partition, message.offset, message.key, value)
            )

    except KafkaError as e:
        print("Kafka error: ", e)

# PYTHONPATH=$(pwd)/.. python3 my_producer.py

import logging
from pathlib import Path

import azure.functions as func
from kafka.errors import KafkaError

import json

from producer.my_producer import (
    send_message,
    send_message_json,
    get_kafka_producer_client,
)
from utils.models import Order


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("New incoming order request")

    try:
        payload = req.get_json()
        order = Order(**payload).__dict__
        logging.info("Order %s", order)

        abs_path = Path(__file__).parent.parent.parent
        print("Path: ", abs_path)
        producer_client = get_kafka_producer_client(
            host="localhost", port=9095, auth_required=True, certs_path=abs_path
        )
        send_message_json(producer_client, order)

        # send_message(message="Hi broker 2", host="localhost", port=9094)
        status_code = 202
        message = {"message": "Order accepted"}
    except ValueError:
        status_code = 422
        message = "Invalid Input"
    except KafkaError as e:
        status_code = 412
        message = e

    return func.HttpResponse(json.dumps(message), status_code=status_code)

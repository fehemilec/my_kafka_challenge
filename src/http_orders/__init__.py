import logging
from pathlib import Path

import azure.functions as func
from kafka.errors import KafkaError

import json

from producer.my_producer import (
    send_message_json,
    get_kafka_producer_client,
    get_kafka_broker,
)
from utils.models import Order


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("New incoming order request")

    try:
        payload = req.get_json()
        order = Order(**payload).__dict__
        logging.info("Order %s", order)

        abs_path = Path(__file__).parent.parent.parent

        broker = get_kafka_broker("1", auth_required=True)
        producer_client = get_kafka_producer_client(abs_path, broker)

        send_message_json(producer_client, order)

        status_code = 202
        message = {"message": "Order accepted"}
    except ValueError:
        status_code = 422
        message = "Invalid Input"
    except KafkaError as e:
        status_code = 412
        message = e

    return func.HttpResponse(json.dumps(message), status_code=status_code)

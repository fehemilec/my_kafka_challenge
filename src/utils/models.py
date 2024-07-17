from pydantic import BaseModel
from collections import namedtuple


class Order(BaseModel):
    orderId: str
    items: int
    price: str


Broker = namedtuple("Broker", ["host", "port", "authentication"])

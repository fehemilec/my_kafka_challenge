from pydantic import BaseModel


class Order(BaseModel):
    orderId: str
    items: int
    price: str

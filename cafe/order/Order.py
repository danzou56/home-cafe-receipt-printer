import datetime
from dataclasses import dataclass

from cafe.order.Item import Item


@dataclass
class Order:
    # timestamp: datetime.datetime
    name: str
    items: list[Item]

    @staticmethod
    def from_dict(data: dict):
        return Order(data["name"], [Item.from_dict(item) for item in data["items"]])

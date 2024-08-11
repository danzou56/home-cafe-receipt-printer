import datetime
from dataclasses import dataclass

from cafe.order.Item import Item


@dataclass
class Order:
    name: str
    timestamp: datetime.datetime
    items: list[Item]

    @staticmethod
    def from_dict(data: dict):
        return Order(
            data["name"],
            datetime.datetime.now(),
            [Item.from_dict(item) for item in data["items"]],
        )

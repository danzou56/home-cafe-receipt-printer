import datetime
from dataclasses import dataclass

from cafe.order.Item import Item


@dataclass(frozen=True)
class Order:
    name: str
    timestamp: datetime.datetime
    items: tuple[Item, ...]

    @staticmethod
    def from_dict(data: dict):
        return Order(
            data["name"],
            datetime.datetime.now(),
            tuple(Item.from_dict(item) for item in data["items"]),
        )

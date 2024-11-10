from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Item:
    name: str
    type: Optional[str]
    # needs to be tuple to be immutable
    sub_items: tuple["Item", ...] = tuple()

    @staticmethod
    def from_dict(data: dict):
        return Item(
            data["name"],
            data.get("type"),
            tuple(Item.from_dict(sub_item) for sub_item in data.get("sub_items", [])),
        )

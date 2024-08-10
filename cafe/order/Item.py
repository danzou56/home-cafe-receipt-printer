from dataclasses import dataclass


@dataclass
class Item:
    name: str
    sub_items: list["Item"]

    @staticmethod
    def from_dict(data: dict):
        return Item(
            data["name"],
            [Item.from_dict(sub_item) for sub_item in data.get("sub_items", [])],
        )

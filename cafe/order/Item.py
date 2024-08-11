from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    # needs to be tuple to be immutable
    sub_items: tuple["Item", ...] = tuple()

    @staticmethod
    def from_dict(data: dict):
        return Item(
            data["name"],
            tuple(Item.from_dict(sub_item) for sub_item in data.get("sub_items", [])),
        )

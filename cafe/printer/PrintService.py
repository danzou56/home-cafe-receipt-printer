import collections
import os
import uuid
from functools import reduce

from cafe.order.Item import Item
from cafe.order.Order import Order
from cafe.printer.PrintClient import PrintClient
from cafe.printer.command.Break import Break
from cafe.printer.command.Command import Command
from cafe.printer.command.TextLn import TextLn


class PrintService:
    _order_number = 0
    orders: dict[str, Order] = dict()

    def __init__(self, print_client: PrintClient):
        self.__client = print_client

    def print(self, order: Order) -> str:
        commands = PrintService.parse_order(order)
        order_id = str(uuid.uuid4())
        self.orders[order_id] = order
        self.__client.print(commands)
        return order_id

    @classmethod
    def parse_order(cls, order: Order) -> list[Command]:
        cls._order_number += 1

        header = [
            TextLn("allicafei", align="center", double_height=True, double_width=True),
            TextLn(os.getenv("PRIVATE_LINE_1", ""), align="center"),
            TextLn(os.getenv("PRIVATE_LINE_2", ""), align="center"),
            Break(),
        ]
        info = [
            TextLn(
                f"{order.name.upper()}",
                double_height=True,
                double_width=True,
            ),
            TextLn(
                f"{order.timestamp.strftime('%m/%d/%Y %I:%M:%S %p')} / #{cls._order_number}"
            ),
            Break(),
        ]
        body = PrintService._parse_top_items(
            list(collections.Counter(order.items).items())
        )

        return header + info + body + [Break(), Break()]

    @staticmethod
    def _parse_top_items(items: list[tuple[Item, int]]) -> list[Command]:
        return reduce(
            list.__add__,
            [
                [
                    TextLn(
                        f"{quantity} x  {item.name}",
                        double_height=True,
                        double_width=True,
                    )
                ]
                + PrintService._parse_items(item.sub_items, 1)
                for (item, quantity) in items
            ],
            [],
        )

    @staticmethod
    def _parse_items(items: tuple[Item, ...], indentation: int = 0) -> list[Command]:
        return reduce(
            list.__add__,
            [
                [TextLn(f"{'\t' * indentation}{item.name}")]
                + PrintService._parse_items(item.sub_items, indentation + 1)
                for item in items
            ],
            [],
        )

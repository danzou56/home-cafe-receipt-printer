import os
from functools import reduce

from cafe.order.Item import Item
from cafe.order.Order import Order
from cafe.printer.PrintClient import PrintClient
from cafe.printer.command.Break import Break
from cafe.printer.command.Command import Command
from cafe.printer.command.TextLn import TextLn


class PrintService:
    _order_number = 0

    def __init__(self, print_client: PrintClient):
        self.__client = print_client

    def print(self, order: Order):
        commands = PrintService._parse_order(order)
        self.__client.print(commands)

    @classmethod
    def _parse_order(cls, order: Order) -> list[Command]:
        cls._order_number += 1

        header = [
            TextLn("Home Cafe", align="center", double_height=True, double_width=True),
            TextLn(os.getenv("PRIVATE_LINE_1", ""), align="center"),
            TextLn(os.getenv("PRIVATE_LINE_2", ""), align="center"),
            Break(),
        ]
        info = [
            TextLn(f"Order for: {order.name}", align="center"),
            TextLn(
                f"{order.timestamp.strftime("%m/%d/%Y %I:%M:%S %p")} / #{cls._order_number}"
            ),
            Break(),
        ]
        body = PrintService._parse_items(order.items)

        return header + info + body + [Break()]

    @staticmethod
    def _parse_items(items: list[Item], indentation: int = 0) -> list[Command]:
        return reduce(
            list.__add__,
            [
                [TextLn(("\t" * indentation) + item.name)]
                + PrintService._parse_items(item.sub_items, indentation + 1)
                for item in items
            ],
            [],
        )

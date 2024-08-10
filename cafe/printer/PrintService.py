from functools import reduce

from cafe.order.Item import Item
from cafe.order.Order import Order
from cafe.printer.PrintClient import PrintClient
from cafe.printer.command.Break import Break
from cafe.printer.command.Command import Command
from cafe.printer.command.TextLn import TextLn


class PrintService:
    def __init__(self, print_client: PrintClient):
        self.__client = print_client

    def print(self, order: Order):
        commands = PrintService._parse_order(order)
        self.__client.print(commands)

    @staticmethod
    def _parse_order(order: Order) -> list[Command]:
        header = [
            Break(),
            TextLn("Home Cafe", align="center", double_height=True, double_width=True),
            Break(),
        ]

        return (
            header
            + [
                TextLn(f"Order for: {order.name}", align="center"),
                TextLn(order.name, align="center"),
            ]
            + PrintService._parse_items(order.items)
        )

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

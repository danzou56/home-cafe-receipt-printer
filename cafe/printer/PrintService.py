from functools import reduce

from cafe.order.Item import Item
from cafe.order.Order import Order
from cafe.printer.PrintClient import PrintClient
from cafe.printer.command.Command import Command
from cafe.printer.command.Text import Text


class PrintService:
    def __init__(self, print_client: PrintClient):
        self.__client = print_client

    def print(self, order: Order):
        commands = PrintService._parse_order(order)
        self.__client.print(commands)

    @staticmethod
    def _parse_order(order: Order) -> list[Command]:
        return [Text(order.name)] + PrintService._parse_items(order.items)

    @staticmethod
    def _parse_items(items: list[Item]) -> list[Command]:
        return reduce(
            list.__add__,
            [
                [Text(item.name)] + PrintService._parse_items(item.sub_items)
                for item in items
            ],
        )

import collections
import datetime
import os
import uuid
from functools import reduce
from itertools import groupby

from cafe.order.Item import Item
from cafe.order.Order import Order
from cafe.printer.PrintClient import PrintClient
from cafe.printer.command.Break import Break
from cafe.printer.command.Command import Command
from cafe.printer.command.TextLn import TextLn


class PrintService:
    _order_number = 0
    orders: dict[str, tuple[int, Order]] = dict()
    _rendered_orders: dict[str, list[Command]] = dict()

    def __init__(self, print_client: PrintClient):
        self.__client = print_client

    def print(self, order_id: str):
        if order_id in PrintService._rendered_orders:
            commands = PrintService._rendered_orders[order_id] + [
                TextLn(
                    "** copy **", align="center", double_height=True, double_width=True
                ),
                Break(),
            ]
        else:
            (order_number, order) = PrintService.orders[order_id]
            commands = PrintService.create_receipt(order, order_number)
            PrintService._rendered_orders[order_id] = commands

            for type, group in groupby(
                sorted(order.items, key=lambda i: i.type), lambda i: i.type
            ):
                if type.lower() == "2":
                    continue
                items_in_group = list(group)
                metadata = PrintService._create_meta(
                    order.name,
                    order_number,
                    order.timestamp,
                )
                body = PrintService._parse_top_items(
                    zip(items_in_group, [1] * len(items_in_group))
                )
                self.__client.print(
                    [TextLn(["food", "drink"][int(type)])]
                    + metadata
                    + body
                    + PrintService._create_footer()
                )

        self.__client.print(commands)

    def create_order(self, order: Order) -> str:
        order_id = str(uuid.uuid4())
        self._order_number += 1
        self.orders[order_id] = (self._order_number, order)
        return order_id

    @staticmethod
    def _create_footer() -> list[Command]:
        return [Break(), Break()]

    @staticmethod
    def _create_header() -> list[Command]:
        header = [
            TextLn("allicafei", align="center", double_height=True, double_width=True),
            # TextLn(os.getenv("PRIVATE_LINE_1", ""), align="center"),
            TextLn(os.getenv("PRIVATE_LINE_2", ""), align="center"),
            Break(),
        ]
        return header

    @staticmethod
    def _create_meta(
        name: str, order_number: int, timestamp: datetime, with_header: bool = False
    ) -> list[Command]:
        header = []
        if with_header:
            header = PrintService._create_header()
        info = [
            TextLn(
                f"{name.upper()}",
                double_height=True,
                double_width=True,
            ),
            TextLn(f"{timestamp.strftime('%m/%d/%Y %I:%M:%S %p')} / #{order_number}"),
            Break(),
        ]
        return header + info

    @staticmethod
    def create_receipt(order: Order, order_number) -> list[Command]:
        info = PrintService._create_meta(
            order.name, order_number, order.timestamp, with_header=True
        )
        body = PrintService._parse_top_items(
            list(collections.Counter(order.items).items())
        )
        footer = PrintService._create_footer()

        return info + body + footer

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
                [
                    TextLn(
                        f"{'\t' * indentation}{item.name}",
                        double_height=True,
                        double_width=True,
                    )
                ]
                + PrintService._parse_items(item.sub_items, indentation + 1)
                for item in items
            ],
            [],
        )

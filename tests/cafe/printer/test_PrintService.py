import datetime

from cafe.order.Item import Item
from cafe.order.Order import Order
from cafe.printer.PrintService import PrintService
from cafe.printer.command.TextLn import TextLn


def test_parse_order():
    commands = PrintService.parse_order(
        Order(
            name="Foo",
            timestamp=datetime.datetime.now(),
            items=[Item(name="Bar", type="Food"), Item(name="Baz", type="Food")],
        )
    )

    text_lns = [command.text for command in commands if isinstance(command, TextLn)]
    assert "1 x  Baz" in text_lns
    assert "1 x  Bar" in text_lns


def test_parse_order_collect():
    commands = PrintService.parse_order(
        Order(
            name="Foo",
            timestamp=datetime.datetime.now(),
            items=[
                Item(name="Bar", type="Food"),
                Item(name="Baz", type="Food"),
                Item(name="Bar", type="Food"),
            ],
        )
    )

    text_lns = [command.text for command in commands if isinstance(command, TextLn)]
    assert "1 x  Baz" in text_lns
    assert "2 x  Bar" in text_lns


def test_parse_order_sub_items():
    commands = PrintService.parse_order(
        Order(
            name="Foo",
            timestamp=datetime.datetime.now(),
            items=[
                Item(
                    name="Bar",
                    type="Food",
                    sub_items=(
                        Item(name="Baz", type="Food"),
                        Item(name="Baz", type="Food"),
                    ),
                )
            ],
        )
    )

    text_lns = [command.text for command in commands if isinstance(command, TextLn)]
    assert "1 x  Bar" in text_lns
    assert text_lns.count("\tBaz") == 2


def test_parse_order_sub_sub_items():
    commands = PrintService.parse_order(
        Order(
            name="Foo",
            timestamp=datetime.datetime.now(),
            items=[
                Item(
                    name="Bar",
                    type="Food",
                    sub_items=(
                        Item(
                            name="Baz",
                            type="Food",
                            sub_items=(
                                Item(name="Baz", type="Food"),
                                Item(name="Baz", type="Food"),
                            ),
                        ),
                    ),
                )
            ],
        )
    )

    text_lns = [command.text for command in commands if isinstance(command, TextLn)]
    assert "1 x  Bar" in text_lns
    assert text_lns.count("\tBaz") == 1
    assert text_lns.count("\t\tBaz") == 2

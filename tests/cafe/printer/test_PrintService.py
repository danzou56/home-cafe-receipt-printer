import datetime

from cafe.order.Item import Item
from cafe.order.Order import Order
from cafe.printer.PrintService import PrintService
from cafe.printer.command.TextLn import TextLn


def test_create_receipt():
    commands = PrintService.create_receipt(
        Order(
            name="Foo",
            timestamp=datetime.datetime.now(),
            items=(Item(name="Bar", type="Food"), Item(name="Baz", type="Food")),
        ),
        0,
    )

    text_lns = [command.text for command in commands if isinstance(command, TextLn)]
    assert "1 x  Baz" in text_lns
    assert "1 x  Bar" in text_lns


def test_create_receipt_collect():
    commands = PrintService.create_receipt(
        Order(
            name="Foo",
            timestamp=datetime.datetime.now(),
            items=(
                Item(name="Bar", type="Food"),
                Item(name="Baz", type="Food"),
                Item(name="Bar", type="Food"),
            ),
        ),
        0,
    )

    text_lns = [command.text for command in commands if isinstance(command, TextLn)]
    assert "1 x  Baz" in text_lns
    assert "2 x  Bar" in text_lns


def test_create_receipt_sub_items():
    commands = PrintService.create_receipt(
        Order(
            name="Foo",
            timestamp=datetime.datetime.now(),
            items=(
                Item(
                    name="Bar",
                    type="Food",
                    sub_items=(
                        Item(name="Baz", type="Food"),
                        Item(name="Baz", type="Food"),
                    ),
                ),
            ),
        ),
        0,
    )

    text_lns = [command.text for command in commands if isinstance(command, TextLn)]
    assert "1 x  Bar" in text_lns
    assert text_lns.count("\tBaz") == 2


def test_create_receipt_sub_sub_items():
    commands = PrintService.create_receipt(
        Order(
            name="Foo",
            timestamp=datetime.datetime.now(),
            items=(
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
                ),
            ),
        ),
        0,
    )

    text_lns = [command.text for command in commands if isinstance(command, TextLn)]
    assert "1 x  Bar" in text_lns
    assert text_lns.count("\tBaz") == 1
    assert text_lns.count("\t\tBaz") == 2

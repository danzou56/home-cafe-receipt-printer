from cafe.order.Item import Item
from cafe.order.Order import Order


def test_order_from_dict():
    order = Order.from_dict({"name": "foo", "items": []})
    assert order.name == "foo"
    assert order.items == ()


def test_order_from_dict_with_items():
    order = Order.from_dict(
        {
            "name": "foo",
            "items": [
                {
                    "name": "bar",
                },
                {
                    "name": "baz",
                },
            ],
        }
    )
    assert order.name == "foo"
    assert order.items == (
        Item(name="bar"),
        Item(name="baz"),
    )

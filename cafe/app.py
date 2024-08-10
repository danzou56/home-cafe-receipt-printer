from escpos.config import Config
from escpos.escpos import Escpos
from escpos.printer import Dummy
from flask import Flask, request

from order.Order import Order
from printer.PrintClient import PrintClient
from printer.PrintService import PrintService

# print_service = PrintService(PrintClient(Dummy()))
c = Config()
c.load("cafe/printer/config.yaml")
raw_printer: Escpos = c.printer()
print_service = PrintService(PrintClient(raw_printer))

app = Flask(__name__)


@app.route("/health-check")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/order", methods=["POST"])
def order():
    content = request.json
    try:
        order = Order.from_dict(content)
    except KeyError as e:
        return "Bad Request", 400
    except TypeError as e:
        return "Bad Request", 400
    print_service.print(order)
    return "", 201

import logging
import os

from dotenv import load_dotenv
from escpos.printer import Dummy
from escpos.config import Config
from escpos.escpos import Escpos
from flask import Flask, request
from flask_cors import cross_origin

from cafe.order.Order import Order
from cafe.printer.PrintClient import PrintClient
from cafe.printer.PrintService import PrintService

load_dotenv()

raw_printer: Escpos
if os.getenv("PRINTER") == "sidewalk":
    c = Config()
    c.load("cafe/printer/config.yaml")
    raw_printer = c.printer()
else:
    raw_printer = Dummy()

print_client = PrintClient(raw_printer)
print_service = PrintService(print_client)

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/health-check")
@cross_origin()
def hello_world():
    return "Hello, World!"


@app.route("/order", methods=["POST"])
@cross_origin()
def order():
    content = request.json
    try:
        order = Order.from_dict(content)
    except KeyError as e:
        logger.error(e)
        return "Bad Request", 400
    except TypeError as e:
        logger.error(e)
        return "Bad Request", 400
    print_client.print(print_service.parse_order(order))
    return "", 201

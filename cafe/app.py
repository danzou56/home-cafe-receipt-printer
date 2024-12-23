import logging
import os

from dotenv import load_dotenv
from escpos.config import Config
from escpos.escpos import Escpos
from escpos.printer import Dummy
from flask import Flask, request
from flask_cors import CORS

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
CORS(app)


@app.route("/health-check")
def hello_world():
    return "Hello, World!"


@app.route("/order", methods=["POST"])
def order():
    logger.info(f"Request: {request.data}")
    content = request.json
    try:
        order = Order.from_dict(content)
        logger.info(f"Order: {order}")
    except KeyError | TypeError as e:
        logger.error(e)
        return "Bad Request", 400
    order_id = print_service.create_order(order)
    print_service.print(order_id)
    return order_id, 201


@app.route("/orders", methods=["GET"])
def get_orders():
    return [{"orderId": k, "order": v} for k, (_, v) in print_service.orders.items()], 200


@app.route("/reprint/<order_id>", methods=["POST"])
def reprint(order_id):
    try:
        print_service.print(order_id)
    except KeyError as e:
        return "No such order ID", 404
    return order_id, 200

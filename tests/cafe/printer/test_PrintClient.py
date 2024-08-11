from escpos.printer import Dummy

from cafe.printer.PrintClient import PrintClient
from cafe.printer.command.TextLn import TextLn


def test_print():
    raw_printer = Dummy()
    client = PrintClient(raw_printer)
    client.print([TextLn("Hello World!")])

    print(raw_printer.output)

from escpos.escpos import Escpos

from cafe.printer.command.Command import Command


class PrintClient:

    def __init__(self, print_impl: Escpos, **kwargs):
        self.__print_impl = print_impl
        self.__defaults = kwargs

    def print(self, commands: list[Command]):
        for command in commands:
            command(self.__print_impl)
        self.__print_impl.cut()

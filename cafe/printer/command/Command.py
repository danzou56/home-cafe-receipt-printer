from abc import ABC

from escpos.escpos import Escpos


class Command(ABC):
    def __call__(self, p: Escpos):
        pass

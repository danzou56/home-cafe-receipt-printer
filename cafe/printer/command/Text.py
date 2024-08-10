from escpos.escpos import Escpos

from Command import Command


class Text(Command):
    def __init__(self, text, formatting=None):
        self.text = text
        self.formatting = formatting

    def __call__(self, p: Escpos):
        p.text(self.text)

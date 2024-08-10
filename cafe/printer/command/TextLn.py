from escpos.escpos import Escpos

from cafe.printer.command.Command import Command


class TextLn(Command):
    def __init__(self, text, **kwargs):
        self.text = text
        self.formatting = kwargs

    def __call__(self, p: Escpos):
        p.set(**self.formatting)
        p.textln(self.text)
        p.set_with_default()

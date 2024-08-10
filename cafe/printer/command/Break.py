from cafe.printer.command.TextLn import TextLn


class Break(TextLn):
    def __init__(self):
        TextLn.__init__(self, "")

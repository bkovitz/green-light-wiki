from Config import config


class CgiOutput:

    def __init__(self, htmlGenerator):
        self.htmlGenerator = htmlGenerator

    def __str__(self):
        return "Content-type: text/html\n\n" + str(self.htmlGenerator)

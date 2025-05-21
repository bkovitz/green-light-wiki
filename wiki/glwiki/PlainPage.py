from RequestedPage import RequestedPage
from File import NonwikiFile
from BadPage import BadPage


class PlainPage(RequestedPage):

    def __init__(self, filename):
        self._f = NonwikiFile(filename)

        if not self._f.exists():
            self.__class__ = BadPage
            BadPage.__init__(self, filename)

    def getCommand(self):
        return "PLAIN"

    def renderHtml(self):
        return "".join(self._f.readlines())

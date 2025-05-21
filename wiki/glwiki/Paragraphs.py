import Chunks


class Paragraph:

    def __init__(self, chunkClass, text=None):
        self._chunkClass = chunkClass
        self._text = text

    def __eq__(self, other):
        return self._chunkClass == other._chunkClass and self._text == other._text

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "<Paragraph chunk=%s text='%s'>" % (
            self._chunkClass.__name__,
            self._text,
        )

    def __hash__(self):
        return hash(self._text)

    def makeChunk(self, page):
        return self._chunkClass(page, self._text)

    def makeChanged(self):
        exec("self._chunkClass = Chunks.Changed%s" % self._chunkClass.__name__)

    def coalesceWith(self, other):
        self._text = self._text + "<br>" + other._text

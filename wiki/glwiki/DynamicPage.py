from StaticPage import StaticPage
from DynamicBodyExtractor import DynamicBodyExtractor


class DynamicPage(StaticPage):

    def _makePageExtractor(self):
        try:
            import WikiCustomizations

            moduleDict = WikiCustomizations.__dict__
        except ImportError:
            moduleDict = None

        return DynamicBodyExtractor(self._f, moduleDict)

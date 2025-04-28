from RequestedPage import RequestedPage
from BadPage import BadPage
from File import File, NonwikiFile
from PipeFromPhp import PipeFromPhp
from BodyExtractor import BodyExtractor
from Html import Html, HtmlTitle, HtmlLink
from HtmlMisc import metaKeywords
from Config import config

class StaticPage(RequestedPage):

   def __init__(self, filename, wikiName=""):
      self._wikiName = wikiName

      if isinstance(filename, File):
         self._f = filename
      elif filename.endswith(".php"):
         self._f = PipeFromPhp(filename)
      else:
         self._f = NonwikiFile(filename)

      if not self._f.exists():
         self.__class__ = BadPage
         BadPage.__init__(self, filename)

      self._cgiLeader = [ "Content-type: text/html" ]


   def getCommand(self):
      return "STATIC"


   def renderHtml(self):
      extractor = self._makePageExtractor()

      cgiLeaderFromExtractor = extractor.cgiLeader()
      if cgiLeaderFromExtractor:
         self.setCgiLeader(cgiLeaderFromExtractor)

      html = Html()
      html.addHeadItem(HtmlTitle(extractor.title()))

      preamble = self.preamble()
      html.addHeadItem(preamble.links())

      links = extractor.links()
      if links:
         html.addHeadItem(links)

      html.add(preamble.body())

      html.add(extractor.body())
      
      return str(html)


   def _makePageExtractor(self):
      return BodyExtractor(self._f)


   def setCgiLeader(self, cgiLeader):
      self._cgiLeader = cgiLeader


   def cgiLeader(self):
      return "\n".join(self._cgiLeader) + "\n"

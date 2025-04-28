from RequestedPage import RequestedPage
from Html import Html, HtmlHolder, H1, HtmlPara, NoRobots, HtmlDiv
from Chunks import Error404Chunk, HtmlPageChunk

class BadPage(RequestedPage):

   def __init__(self, url):
      self._url = url


   def getCommand(self):
      return "BAD"


   def cgiLeader(self):
      return \
"""Content-type: text/html
Status: 404
"""


   """
   def renderHtml(self):
      result = Html("Page not found")
      result.addHeadItem(NoRobots())
      result.addHeadItem(self.preamble().links())
      result.add(self.preamble().body())
      result.add(self.htmlBody())
      return result
   """

   def renderHtml(self):
      return HtmlPageChunk(
         self,
         "Page not found",
         self.preamble().links(),
         None,
         NoRobots(),
         self.htmlBody()
      )


   def htmlBody(self):
      return Error404Chunk(self, self._url)

from urllib.parse import unquote
from time import time

from RequestedPage import RequestedPage
from Chunks import HtmlPageChunk, WikiPageBodyChunk, ContentChunk, \
   TopChunk, BottomChunk, BadVersionNumberChunk
from WikiRepository import WikiRepository
import SessionDatabase
from UnsmashWords import unsmashWords
from Config import config
from Html import HtmlLink, HtmlDiv, HtmlPara, HtmlAnchor, HtmlImage, Class
from HtmlMisc import metaKeywords
from VersionedFile2 import BadVersionException


class WikiPage(RequestedPage):

   def __init__(self, environment):
      self._environment = environment
      self._repository = WikiRepository(environment.getWikiName())
      self._pageName = parsePageBaseName(environment.getPageName())
      if len(self._pageName) == 0:
         self._pageName = config.defaultPage(environment.getWikiName())

      self.setCookie(SessionDatabase.makeCookie(self.getSessionId()))


   def renderHtml(self):
      self.makeData()

      return HtmlPageChunk(
         self,
         self.getTitle(),
         self.getStyleSheets(),
         self.getKeywords(),
         self.getMetas(),
         self.getBody()
      )


   def getTitle(self):
      try:
         return self._title
      except AttributeError:
         return unsmashWords(self.getPageName())


   def getStyleSheets(self):  return self._styleSheets
   def getKeywords(self):     return self._keywords
   def getMetas(self):        return self._metas
   def getBody(self):         return self._body


   def getMessage(self):
      return None


   def makeData(self):
      self.makeTitle()
      self.makeStyleSheets()
      self.makeKeywords()
      self.makeMetas()
      self.makeBody()


   def makeTitle(self):
      self._title = unsmashWords(self.getPageName())


   def makeStyleSheets(self):
      stylesheet = config.get(self.getWikiName(), "stylesheet", None)
      if stylesheet:
         self._styleSheets = HtmlLink(
            rel="STYLESHEET",
            href=stylesheet,
            type="text/css"
         )
      else:
         self._styleSheets = None


   def makeKeywords(self):
      keywords = config.get(self.getWikiName(), "keywords")
      if keywords:
         self._keywords = metaKeywords(self.getWikiName())
      else:
         self._keywords = None


   def makeMetas(self):
      self._metas = None


   def makeBody(self):
      try:
         self._body = WikiPageBodyChunk(
            self,
            self.top(),
            self.getMessage(),
            self.getContent(),
            self.getButtons()
         )
      #except BadVersionException, e:
      except BadVersionException as e:
         self._body = WikiPageBodyChunk(
            self,
            self.top(),
            BadVersionNumberChunk(self, e.versionNum),
            None,
            BottomChunk(self, self.buttons())
         )


   def getContent(self):
      return ContentChunk(self, self.contentParas()),


   def top(self):
      return TopChunk(
         self,
         self.getTitle(),
         self.homeLink(),
         self.logo()
      )


   def logo(self):
      logo = config.logo(self.getWikiName())
      if logo:
         return HtmlPara(
            HtmlAnchor(
               config.homeUrl(self.getWikiName()),
               HtmlImage(logo)
            ),
            Class("logo")
         )


   def getButtons(self):
      return BottomChunk(self, self.buttons())


   def homeLink(self):
      defaultPageName = config.defaultPage(self.getWikiName())
      if unsmashWords(defaultPageName) == unsmashWords(self.getPageName()):
         return "&nbsp;"
      else:
         return HtmlAnchor(
            config.homeUrl(self.getWikiName()),
            unsmashWords(config.defaultPage(self.getWikiName()))
         )



   def getWikiName(self):
      return self._environment.getWikiName()


   def getPageName(self):
      return self._pageName


   def getRepository(self):
      return self._repository


   def getQueryDict(self):
      return self._environment.getQueryDict()


   def getPageUrl(self):
      return config.makeUrl(
         self.getWikiName(),
         self.getPageName()
      )


   def getFormDict(self):
      return self._environment.getFormDict()


   def getUserName(self):
      return self._environment.getUserName()


   def getInputFile(self):
      return self._environment.getInputFile()


   def getIpAddress(self):
      return self._environment.getIpAddress()


   def getSessionId(self):
      sessionId = self._environment.getSessionId()
      if not sessionId:
         sessionId = SessionDatabase.makeSession(
            int(time()),
            self._environment.getIpAddress()
         )

      return sessionId


def parsePageBaseName(fullPageName):
   elements = fullPageName.split("/")
   return unquote(elements[-1])

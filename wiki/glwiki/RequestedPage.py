import os

from File import File
from BodyExtractor import BodyExtractor
from Misc import makeList


class RequestedPage:

   def action(self):
      pass # override if the page "does" something before it renders


   def getCommand(self):
      raise "abstract class: must override method"


   def getPageName(self):
      raise "abstract class: must override method"


   def renderCgi(self):
      html = str(self.renderHtml())
      return self.cgiLeader() + "\n" + html


   def cgiLeader(self):
      result = "Content-type: text/html\n"
      setCookie = self.getCookie()
      if setCookie:
         result += str(setCookie) + "\n"

      return result


   def preamble(self):
      if "_preamble" not in self.__dict__:
         self._preamble = BodyExtractor(File("preamble.html"))
      return self._preamble


   def setCookie(self, cookie):
      self._cookie = cookie


   def getCookie(self):
      try:
         return self._cookie
      except AttributeError:
         return None

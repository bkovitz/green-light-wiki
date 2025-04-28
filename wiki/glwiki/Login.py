from time import time

from WikiPage import WikiPage
import SessionDatabase
from SessionDatabase import BadSessionId
from Config import config

class Login(WikiPage):
   
   def getCommand(self):
      return "LOGIN"


   def action(self):
      userName = self.getFormDict()["userName"]
      try:
         SessionDatabase.setUserName(self.getSessionId(), userName)
      except BadSessionId:
         self._newSessionId = SessionDatabase.makeSession(
            int(time()),
            self._environment.getIpAddress()
         ) #TODO: OAOO
         SessionDatabase.setUserName(self._newSessionId, userName)


   def cgiLeader(self):
      result = \
"""Status: 303
Location: %s?action=edit
""" % config.makeUrl(self.getWikiName(), self.getPageName())

      try:
         result += str(SessionDatabase.makeCookie(self._newSessionId)) + "\n"
      except AttributeError:
         pass

      return result


   def renderHtml(self):
      return ""

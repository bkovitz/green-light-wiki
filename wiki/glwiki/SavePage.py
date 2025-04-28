from time import time

from WikiPage import WikiPage
from Config import config
from Html import Html, HtmlAnchor, HtmlTextArea, HtmlRefresh, \
   HtmlPara, HtmlDiv, NoRobots
from VersionedFile2 import VersionedFile2
from WikiText2 import WikiText2
import RecentChanges
import SessionDatabase
from SessionDatabase import BadSessionId
from Chunks import SuccessfulSaveChunk, CouldntSaveDueToConflictChunk, \
   WikiPageBodyChunk, EditChunk

class SavePage(WikiPage):

   def getCommand(self):
      return "SAVE"


   def action(self):
      if self._okToSave():
         self._save()
         self._savedSuccessfully = True
         try:
            self._setPendingMessage(SuccessfulSaveChunk)
         except BadSessionId:
            pass
      else:
         self._savedSuccessfully = False


   def _setPendingMessage(self, messageChunkClass):
      SessionDatabase.setPendingMessage(
         self.getSessionId(),
         messageChunkClass,
         (self.getTitle(),)
      )


   def cgiLeader(self):
      if self.savedSuccessfully():
         return \
"""Content-type: text/html
Status: 303
Location: %s
""" % self.getPageUrl()
      else:
         return WikiPage.cgiLeader(self)


   def makeBody(self):
      if self.savedSuccessfully():
         self._body = "<p>Saved successfully. Redirecting...</p>"
      else:
         self._body = WikiPageBodyChunk(
            self,
            self.top(),
            self.getMessage(),
            EditChunk(self, self._rawText()),
            None
         )


   def savedSuccessfully(self):
      return self._savedSuccessfully


   def getMessage(self):
      url = config.makeUrl(
         self.getWikiName(),
         self.getPageName()
      )

      if self.savedSuccessfully():
         return None
      else:
         return CouldntSaveDueToConflictChunk(
            self,
            self.getPageName(),
            self._previousAuthor(),
            self.getRepository()
         )


   def _readlines(self):
      f = self._openForReading()
      if f:
         versionManager = VersionedFile2(f)
         result = versionManager.getLatestVersion()
         f.close()
      else:
         result = [""]

      return result


   def _okToSave(self):
      return int(self._origVersion()) == int(self._maxVersionNum())


   def _save(self):
      f = self._openForWriting()
      versionManager = VersionedFile2(f)
      versionManager.writeNewVersion(self.getUserName(), self.text())
      f.close()

      RecentChanges.logChange2(
         self.getWikiName(),
         self.getUserName(),
         self.getPageName()
      )


   def _origVersion(self):
      if self.getFormDict():
         return self.getFormDict().get("origVersion", 0)
      else:
         return 0


   def text(self):
         return [ line.replace("\r", "") for line in self.getInputFile().readlines() ]


   def _rawText(self):
         return "".join(self.getInputFile().readlines())


   def _previousAuthor(self):
      f = self._openForReading()
      if f:
         versionManager = VersionedFile2(f)
         result = versionManager.getLatestAuthor()
         f.close()
      else:
         result = "(unknown)"

      return result


   def _savedNotice(self):
      return (
         config.noticeFontStart(self.wikiCommand.wikiName)
         +
         "successfully saved your changes"
         +
         config.noticeFontEnd(self.wikiCommand.wikiName)
      )


   def _maxVersionNum(self):
      f = self._openForReading()
      if f:
         versionManager = VersionedFile2(f)
         result = versionManager.getLatestVersionNum()
         f.close()
      else:
         result = 0

      return result


   def _openForReading(self):  #TODO: OAOO
      return self._repository.pageFile(self.getPageName()).openForReading()


   def _openForWriting(self):  #TODO: OAOO
      return self._repository.pageFile(self.getPageName()).openForWriting()

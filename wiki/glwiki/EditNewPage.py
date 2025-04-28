from EditPage import EditPage
from UnsmashWords import unsmashWords
from Html import HtmlPara, HtmlAnchor
from Config import config

class EditNewPage(EditPage):

   def getCommand(self):
      return "NEW"


   def text(self):
      return "Describe " + unsmashWords(self._pageName) + " here."


   def loginDiv(self):
      return self.genericLoginDiv(
         "edit",
         HtmlPara([
            "You are attempting to create a new page called ",
            HtmlAnchor(   #TODO: add the appropriate CLASS
               config.makeUrl(
                  self.getWikiName(),
                  self.getPageName(),
               ),
               unsmashWords(self.getPageName())
            ),
            ". You need to log in before you can do this."
         ])
      )



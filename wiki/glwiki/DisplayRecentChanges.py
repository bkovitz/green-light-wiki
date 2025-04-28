from DisplayPage import DisplayPage
import RecentChanges
from Html import OneRowTable, ButtonLink
from Config import config


class DisplayRecentChanges(DisplayPage):

   def contentParas(self):
      return RecentChanges.renderHtml(self.getWikiName())


   def buttons(self):
      return [
         self.homeButton(),
         self.allButton()
      ]


   def getTitle(self):
      return "Recent Changes"

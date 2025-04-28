from DisplayPage import DisplayPage
import AllPages
from Html import OneRowTable, ButtonLink
from Config import config


class DisplayAllPages(DisplayPage):

   def contentParas(self):
      return AllPages.renderHtml(self.getRepository())


   def buttons(self):
      return [
         self.homeButton(),
         self.recentButton()
      ]

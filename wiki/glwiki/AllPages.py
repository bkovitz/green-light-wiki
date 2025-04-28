from Config import config
from WordReplacer import makeAnchor
from UnsmashWords import unsmashWords
from Html import HtmlPara, Class
from HtmlMisc import _itemClass


class PageName:

   def __init__(self, linkName):
      self.linkName = linkName
      self.unsmashedName = unsmashWords(linkName)

   def __cmp__(self, other):
      return cmp(self.unsmashedName, other.unsmashedName)


def renderHtml(wikiRepository):
   pageNames = [
      PageName(pageName) for pageName in wikiRepository.allPageNames()
   ]
   pageNames.sort()

   return [
      HtmlPara(
         makeAnchor(
            config.makeUrl(wikiRepository.getWikiName(), pageName.linkName),
            pageName.unsmashedName
         ),
         _itemClass
      )
         for pageName in pageNames
   ]

from Config import config
from Html import HtmlMeta, Class


_itemClass = Class("item")

def metaKeywords(wikiName):
   return HtmlMeta("keywords", config.get(wikiName, "keywords"))



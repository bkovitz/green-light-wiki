from BadPage import BadPage
from StaticPage import StaticPage
from DynamicPage import DynamicPage
from MakeWikiPage import makeWikiPage
from PlainPage import PlainPage
from Config import config


def badPageFactory(environment):
   return BadPage(environment.getUri())


def staticPageFactory(environment):
   return StaticPage(environment.getPageName(), environment.getWikiName())


def wikiPage2Factory(environment):
   return makeWikiPage(environment)


def plainPageFactory(environment):
   return PlainPage(environment.getPageName())


def dynamicPageFactory(environment):
   return DynamicPage(environment.getPageName())


_pageFactories = {
   "BAD": badPageFactory,
   "STATIC": staticPageFactory,
   "WIKI": wikiPage2Factory,
   "PLAIN": plainPageFactory,
   "DYNAMIC": dynamicPageFactory,
}


def getPageFactory(fileType):
   return _pageFactories[fileType]

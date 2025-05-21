from teest import *
import utMisc, re, shelve, time
from io import StringIO
from Html import HtmlTable, HtmlRow, HtmlDatum, HtmlAnchor, HtmlHolder

from RecentChanges import logChange, retrieveChanges, MostRecentChangeToAPage, \
                          _renderChanges, _renderChangesInHtml

from WikiCommand import WikiCommand

class ut_RecentChanges:

   def __init__(self):
      self.filename = "TESTDATA.RecentChanges"


   def setUp(self):
      self._removeShelf()


   def tearDown(self):
      # self._removeShelf()
      pass


   def testlogChange(self): #TODO

      # log a change

      command = WikiCommand(
         "SAVE",
         "TESTDATA",
         "PageTitle",
         None,
         "MrUser",
      )

      logChange(command)

      recentChanges = retrieveChanges("TESTDATA", 1)

      TEST_EQ(1, len(recentChanges))

      TEST_EQ("PageTitle", recentChanges[0].pageName)
      TEST_EQ("MrUser", recentChanges[0].userName)

      # log a change of a different page

      command = WikiCommand(
         "SAVE",
         "TESTDATA",
         "OtherPage",
         None,
         "GeorgeGibbons",
      )

      logChange(command)

      recentChanges = retrieveChanges("TESTDATA", 10)

      TEST_EQ(2, len(recentChanges))

      TEST_EQ("OtherPage", recentChanges[0].pageName)
      TEST_EQ("GeorgeGibbons", recentChanges[0].userName)

      TEST_EQ("PageTitle", recentChanges[1].pageName)
      TEST_EQ("MrUser", recentChanges[1].userName)

      # log a change of an existing page

      command = WikiCommand(
         "SAVE",
         "TESTDATA",
         "PageTitle",
         None,
         "CalWorthington",
      )

      logChange(command)

      recentChanges = retrieveChanges("TESTDATA", 10)

      TEST_EQ(2, len(recentChanges))

      TEST_EQ("PageTitle", recentChanges[0].pageName)
      TEST_EQ("CalWorthington", recentChanges[0].userName)

      TEST_EQ("OtherPage", recentChanges[1].pageName)
      TEST_EQ("GeorgeGibbons", recentChanges[1].userName)


   def testRender(self):
      items = [
         MostRecentChangeToAPage(
            "OnePage",
            "GeorgeGibbons",
            _t((2003, 7, 24, 15, 50, 21))
         ),
         MostRecentChangeToAPage(
            "SecondPage",
            "DrJohnMittens",
            _t((2003, 7, 24, 12, 50, 21))
         ),
      ]

      expect = \
"""Thursday, July 24

 15:50 [OnePage] . . . . . . [GeorgeGibbons]
 12:50 [SecondPage] . . . . . . [DrJohnMittens]
"""
      TEST_EQ(expect, _renderChanges(items))


   def testRenderHtml(self):
      items = [
         MostRecentChangeToAPage(
            "OnePage",
            "GeorgeGibbons",
            _t((2003, 7, 24, 15, 50, 21))
         ),
         MostRecentChangeToAPage(
            "SecondPage",
            "121.12.131.14",
            _t((2003, 7, 24, 12, 50, 21))
         ),
      ]

      expect = HtmlHolder([
         '<H2>Thursday, July 24</H2>\n',
         '<P CLASS="item">15:50 %s . . . . . . %s</P>\n' % (
            HtmlAnchor("http://greenlightwiki.com/OnePage", "One Page"),
            HtmlAnchor("http://greenlightwiki.com/GeorgeGibbons", "George Gibbons")),
         '<P CLASS="item">12:50 %s . . . . . . %s</P>\n' % (
            HtmlAnchor("http://greenlightwiki.com/SecondPage", "Second Page"),
            "121.12.131.14",
         ),
      ])

      TEST_EQ(str(expect), str(_renderChangesInHtml(items, "TESTDATA")))


   def _removeShelf(self):
      utMisc.forceRemove(self.filename)


def _t(halfTup):
   return _mkgmtime(halfTup + (0, 0, -1))


def _mkgmtime(tup):
   return time.mktime(tup)

from teest import *
from utMisc import FakeEnvironment, forceRemove

from WikiPage import WikiPage

from WikiRepository import WikiRepository
from Chunks import HtmlPageChunk
from DisplayPage import DisplayPage


class FakeChunkPage(WikiPage):
   def makeTitle(self):
      self._title = "Empty Page"

   def makeStyleSheets(self):
      self._styleSheets = \
         '<link rel="stylesheet" href="wiki.css" type="text/css">'

   def makeKeywords(self):
      self._keywords = '<META NAME="keywords" CONTENT="wiki, unit test">'

   def makeBody(self):
      self._body = '<body>Fake body text.</body>'


class ut_WikiPage:

   def tearDown(self):
      forceRemove("preamble.html")


   def testFakeRenderHtml(self):
      page = FakeChunkPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageTitle",
         "George Gibbons"
      ))

      got = page.renderHtml()
      TEST_EQ(HtmlPageChunk, got.__class__)
      TEST_EQ("Empty Page", got.title)
      TEST_EQ(
         '<link rel="stylesheet" href="wiki.css" type="text/css">',
         got.stylesheets
      )
      TEST_EQ('<META NAME="keywords" CONTENT="wiki, unit test">', got.keywords)
      TEST_EQ('<body>Fake body text.</body>', got.body)


   def teestPreamble(self):
      # BEN 23-Jun-2004 Wasn't sure I should delete this.  It fails on OS X.
      # I can't remember if it's still in use on sbml.org or if we replaced
      # the preamble with something else.
      self._makePreamble()
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageTitle",
         "George Gibbons"
      ))

      got = str(page.renderHtml())
      print got #DEBUG
      TEST(got.find("SHORTCUT ICON") >= 0)
      TEST(got.find("Preamble text") >= 0)


   def _makePreamble(self):
      f = file("preamble.html", "w+")
      f.write(
"""<HTML>
<HEAD>
  <link rel="SHORTCUT ICON" href="/favicon.ico">
  <link rel="stylesheet" href="sitewide.css" type="text/css">
</HEAD>
<BODY>
  <p>Preamble text</p>
</BODY>
</HTML>
""")
      f.close()

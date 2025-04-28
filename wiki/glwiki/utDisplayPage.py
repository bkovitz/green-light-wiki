from teest import *
from utMisc import FakeEnvironment
from Misc import forceRemove

from DisplayPage import DisplayPage

from WikiRepository import WikiRepository
from Html import Html, HtmlTable, HtmlRow, HtmlDatum, HtmlLink, \
   HtmlAttribute, OneRowTable, HtmlForm, HtmlInputSubmit, HtmlInputHidden, \
   ButtonLink, HtmlMeta, HtmlAnchor
from VersionedFile2 import VersionedFile2, BadVersionException
from StringIO import StringIO
from Chunks import BadVersionNumberChunk, LinkToExistingPageChunk, \
   VersionInfoChunk, TopChunk, ParagraphChunk, ChangedParagraphChunk, \
   OrderedListItemChunk


class ut_DisplayPage:

   def testBasics(self):
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageTitle",
         "George Gibbons"
      ))
      chunk = page.renderHtml()
      # no crash means pass

      
   def testContentParas(self):
      self._createFileToDisplay()

      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageTitle",
         "George Gibbons"
      ))

      expect = [
         "<p>First line</p>\n",
         "<p>Second line</p>\n",
      ]

      TEST_EQ(expect, [str(para) for para in page.contentParas()])


   def _createFileToDisplay(self):
      forceRemove("TESTWIKI/PageTitle")

      originalText = "First line\n\nSecond line\n"
      wikiFile = VersionedFile2(file("TESTWIKI/PageTitle", "w+"))
      wikiFile.writeNewVersion(
         "Dr. John Mittens",
         StringIO(originalText)
      )
      wikiFile.close()


   def testRequestedVersion(self):
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageWithTwoVersions",
         "George Gibbons",
         queryString="version=1",
      ))

      expect = [
         "<p>The first version of this file.</p>\n",
      ]

      TEST_EQ(expect, [str(para) for para in page.contentParas()])

      buttons = page.buttons()
      got = buttons[5]

      TEST_EQ(VersionInfoChunk, got.__class__)
      TEST_EQ("1", got.versionNum)
      TEST_EQ("2003-Oct-09 01:22 UTC", got.date)
      TEST_EQ("Dr. John Mittens", got.author)


   def testBadVersionNumber(self):
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageWithTwoVersions",
         "George Gibbons",
         queryString="version=3",
      ))

      page.renderHtml()

      TEST_EQ(BadVersionNumberChunk, page.getBody().message.__class__)
      TEST_EQ(3, page.getBody().message.versionNum)


   def testVersionInfo(self):
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageWithTwoVersions",
         "George Gibbons",
      ))

      buttons = page.buttons()
      got = buttons[5]

      TEST_EQ(VersionInfoChunk, got.__class__)
      TEST_EQ("2", got.versionNum)
      TEST_EQ("2003-Oct-13 01:10 UTC", got.date)
      TEST_EQ("Buford Rhizomes", got.author)

      str(got)  #exercise HTML generation


   def testVersionInfoWithTenVersions(self):
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageWithTenVersions",
         "George Gibbons",
      ))

      buttons = page.buttons()
      got = buttons[5]

      TEST_EQ(VersionInfoChunk, got.__class__)
      TEST_EQ("10", got.versionNum)
      TEST_EQ("2003-Oct-18 01:10 UTC", got.date)
      TEST_EQ("Tenth Author", got.author)

      str(got)  #exercise HTML generation


   def testVersionInfoWithPlainFile(self):
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageThatExists",
         "George Gibbons",
      ))

      buttons = page.buttons()
      got = buttons[5]

      TEST_EQ(VersionInfoChunk, got.__class__)
      TEST_EQ("1", str(got.versionNum))
      #TODO: make a FakeWikiRepository class that lets us set the date on a file
      #TEST_EQ("2003-Aug-31 22:11 UTC", got.versionDate)
      TEST_EQ("(unknown)", got.author)

      str(got)  #exercise HTML generation


   #TODO: version info with ?version=


   def testTop(self):
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageThatExists",
         "George Gibbons",
      ))

      page.makeData()
      got = page.top()

      TEST_EQ(TopChunk, got.__class__)
      TEST_EQ("Page That Exists", got.title)
      TEST_EQ('<P CLASS="logo"><A HREF="http://greenlightwiki.com/WelcomePage"><IMG SRC="http://greenlightwiki.com/b5WikiLogo.gif" BORDER=0></A></P>\n', str(got.logo))
      TEST_EQ('<A HREF="http://greenlightwiki.com/WelcomePage">Welcome Page</A>', str(got.homeLink))


   def testChangeBars(self):
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageWithTwoAuthors",
         "George Gibbons",
      ))

      expect = [
         ParagraphChunk(page, "george one"),
         ChangedParagraphChunk(page, "john one"),
         ParagraphChunk(page, "george three"),
         ChangedParagraphChunk(page, "john two"),
      ]

      TEST_EQ(expect, page.contentParas())


   def testNumberedList(self):
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageWithNumberedLists",
         "George Gibbons",
      ))

      p1 = OrderedListItemChunk(page, "first item")
      p2 = OrderedListItemChunk(page, "second item")
      p3 = OrderedListItemChunk(page, "third item")
      p4 = ParagraphChunk(page, "list break")
      p5 = OrderedListItemChunk(page, "new first item")

      p1.number = 1
      p2.number = 2
      p3.number = 3
      p5.number = 1

      TEST_EQ([p1, p2, p3, p4, p5], page.contentParas())

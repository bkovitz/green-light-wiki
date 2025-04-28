from teest import *
import utMisc

from WikiRepository import WikiRepository, _bestMatch


class ut_WikiRepository:

   def setUp(self):
      utMisc.resetConfig()


   def testMakeUrl(self):
      repository = WikiRepository("TESTDATA")

      expect = "http://greenlightwiki.com/Page_Match"

      TEST_EQ(expect, repository.makeUrl("Page_Match"))


   def testQuoteSpecialUrlChars(self):
      repository = WikiRepository("TESTDATA")

      pageName = 'This/That_or_"What"?'
      expect = "http://greenlightwiki.com/This%2FThat_or_%22What%22%3F"

      TEST_EQ(expect, repository.makeUrl(pageName))


   def testMatchMatching(self):
      names = [
         "Blah",
         "HackathonNotes",
         "Some_Page",
      ]

      TEST_EQ("HackathonNotes", _bestMatch(names, "Hackathon_Notes"))
      TEST_EQ("HackathonNotes", _bestMatch(names, "hackathonnotes"))
      TEST_EQ("HackathonNotes", _bestMatch(names, "hackathon_notes"))
      TEST_EQ("Some_Page", _bestMatch(names, "SomePage"))
      TEST_EQ("Some_Page", _bestMatch(names, "some_page"))
      TEST_EQ("Some_Page", _bestMatch(names, "SOME_PAGE"))
      TEST_EQ(None, _bestMatch(names, "somepage"))
      TEST_EQ(None, _bestMatch(names, "Nonexistent_Page"))

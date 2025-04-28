from teest import *
from utMisc import FakeEnvironment

from VersionHistoryPage import VersionHistoryPage

from Chunks import VersionHistoryItemChunk, VersionHistoryChunk
from WikiRepository import WikiRepository


class ut_VersionHistoryPage:

   def testAll(self):
      page = VersionHistoryPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageWithTwoVersions",
         "George Gibbons",
      ))

      page.makeData()

      got = page.getBody().content

      expectItem1 = VersionHistoryItemChunk(
         page,
         versionNum=1,
         date="2003.10.9.1.22.17",
         author="Dr. John Mittens",
         plusMinus="+1"
      )
         
      expectItem2 = VersionHistoryItemChunk(
         page,
         versionNum=2,
         date="2003.10.13.1.10.15",
         author="Buford Rhizomes",
         plusMinus="+1 -1"
      )

      expect = VersionHistoryChunk(page, [expectItem1, expectItem2])

      TEST_EQ(2, len(expect.historyItems))
      TEST_EQ(expectItem1, got.historyItems[0])
      TEST_EQ(expectItem2, got.historyItems[1])
      TEST_EQ(expect, got)

      str(got)

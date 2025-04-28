from teest import *
from utMisc import FakeEnvironment

from Chunks import WikiPageBodyChunk

from StringIO import StringIO
from DisplayPage import DisplayPage
from WikiRepository import WikiRepository
from BodyExtractor import BodyExtractor


class ut_Chunk:

   def testPreamble(self):
      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageThatExists",
         "George Gibbons",
      ))

      page._preamble = BodyExtractor(StringIO(
"""<html><head>
  <LINK REL="STYLESHEET" HREF="/ncbc/wiki.css" TYPE="text/css">
</head>
<body>
   <p>Preamble paragraph</p>
</body>
</html>
"""))

      expect = \
"""\n   <p>Preamble paragraph</P>

TOP
MESSAGE
CONTENT
BOTTOM
"""
      got = WikiPageBodyChunk(page, "TOP", "MESSAGE", "CONTENT", "BOTTOM")

      TEST_EQ(expect, str(got))

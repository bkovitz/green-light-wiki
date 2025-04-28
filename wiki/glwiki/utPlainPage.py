from teest import *

from PlainPage import PlainPage
from BadPage import BadPage

class ut_PlainPage:

   def testDisplayPlainPage(self):
      page = PlainPage("TESTPLAIN/htmlTest.html")

      expect = \
"""Content-type: text/html

<HTML>
<HEAD>
   <TITLE>test title</TITLE>
</HEAD>
<BODY>
   Some body text begins here&#150;with an ampersand: &amp;.
   <P>
   Some more body <A HREF="http://nothing.com">text</A>.
</BODY>
</HTML>
"""
      TEST_EQ(expect, page.renderCgi())


   def testNonexistentPlainPage(self):
      page = PlainPage("TESTPLAIN/nonexistent.html")

      TEST_EQ(BadPage, page.__class__)

      got = page.renderCgi()

      TEST(got.find("TESTPLAIN/nonexistent.html") >= 0)
      TEST(got.find("Status: 404\n") >= 0)

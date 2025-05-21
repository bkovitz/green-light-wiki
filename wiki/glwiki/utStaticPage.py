from teest import *
from utMisc import FileFromString
from io import StringIO

from StaticPage import StaticPage
from BadPage import BadPage

class ut_StaticPage:

   def testDisplayStaticPage(self):
      page = StaticPage("TESTSTATIC/htmlTest.html")

      # TODO: add a test for preamble: that's the main purpose of StaticPage!
      expect = \
"""Content-type: text/html

<HTML><HEAD>
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


   def testNonexistentStaticPage(self):
      page = StaticPage("TESTSTATIC/nonexistent.html")

      TEST_EQ(BadPage, page.__class__)

      got = page.renderCgi()

      TEST(got.find("TESTSTATIC/nonexistent.html") >= 0)
      TEST(got.find("Status: 404\n") >= 0)


   def testCookie(self):
      html = \
"""<HTML><HEAD>
  <TITLE>test</TITLE>
</HEAD>
<BODY>
  test body
</BODY>
</HTML>
"""

      page = StaticPage(FileFromString(html))
      page.setCgiLeader(["Set-Cookie: blah=blee"])

      expect = \
"""Set-Cookie: blah=blee

""" + html

      TEST_EQ(expect, page.renderCgi())

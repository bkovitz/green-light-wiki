from teest import *
from utMisc import FileFromString
from io import StringIO

from DynamicPage import DynamicPage


class ut_DynamicPage:

    def testDisplayDynamicPage(self):
        page = DynamicPage("TESTSTATIC/dynamicTest.html")

        # TODO: add a test for preamble: that's the main purpose of StaticPage!
        expect = """Content-type: text/html

<HTML><HEAD>
  <TITLE>test title</TITLE>
</HEAD>
<BODY>
   Some body text with SAMPLE in the middle.
</BODY>
</HTML>
"""
        TEST_EQ(expect, page.renderCgi())

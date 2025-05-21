from teest import *
from io import StringIO

from HtmlReader import HtmlReader


class ut_HtmlReader:

    def testReproducingHtml(self):
        input = """<HTML><HEAD><TITLE>ignored title</TITLE></HEAD>
<BODY>
   Some body text begins here&#150;with an ampersand: &amp;.
   <P>
   Some more body <A HREF="http://nothing.com">text</A>.
</BODY>
</HTML>
"""

        expect = """<HTML><HEAD>
  <TITLE>ignored title</TITLE>
</HEAD>
<BODY>
   Some body text begins here&#150;with an ampersand: &amp;.
   <P>
   Some more body <A HREF="http://nothing.com">text</A>.
</BODY>
</HTML>
"""

        reader = HtmlReader(StringIO(input))
        internalHtml = reader.extract()

        TEST_EQ(expect, str(internalHtml))

    def testModifyingHtml(self):
        input = """<HTML><HEAD><TITLE>ignored title</TITLE></HEAD>
<BODY>
   Some body text begins here&#150;with an ampersand: &amp;.
   <P>
   Some more body <A HREF="http://nothing.com">text</A>.
</BODY>
</HTML>
"""

        expect = """<HTML><HEAD>
  <TITLE>ignored title</TITLE>
</HEAD>
<BODY>
   Some body text begins here&#150;with an ampersand: &amp;.
   <P>
   Some more body <A HREF="http://nothing.com">text</A>.
   An extra line.
</BODY>
</HTML>
"""

        reader = HtmlReader(StringIO(input))
        internalHtml = reader.extract()
        internalHtml.add("   An extra line.\n")

        TEST_EQ(expect, str(internalHtml))

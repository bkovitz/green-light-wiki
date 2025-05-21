from teest import *

from StoryRectangle import StoryRectangle
from Html import HtmlPara


class ut_StoryRectangle:

    def testAll(self):
        rect = StoryRectangle(HtmlPara("contents"))

        expect = """<TABLE CLASS="story" CELLPADDING="0" CELLSPACING="0">
  <TR>
    <TD CLASS="story-tl"></TD>
    <TD CLASS="story-t"></TD>
    <TD CLASS="story-tr"></TD>
  </TR>
  <TR>
    <TD CLASS="story-l"></TD>
    <TD>
      <P>contents</P>
    </TD>
    <TD CLASS="story-r"></TD>
  </TR>
  <TR>
    <TD CLASS="story-bl"></TD>
    <TD CLASS="story-b"></TD>
    <TD CLASS="story-br"></TD>
  </TR>
</TABLE>
"""

        TEST_EQ(expect, str(rect))

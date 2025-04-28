from teest import *
from os.path import normpath
import RecentChanges, utMisc
from WikiCommand import WikiCommand
from WikiRepository import WikiRepository, NullRepository
from LatexImage import LatexImage

from WikiText2 import WikiText2
from Html import ListRow, HtmlAnchor, Span
from Paragraphs import Paragraph
from Chunks import ParagraphChunk, HorizontalRuleChunk, Heading1Chunk, \
   Heading2Chunk, Heading3Chunk, Heading4Chunk, Heading5Chunk, \
   UnorderedListItemChunk, OrderedListItemChunk

testRepository = NullRepository()
testRepository.recentChangesFilename = lambda: "TESTDATA.RecentChanges"


class ut_WikiText2:

   def testSimpleRender(self):
      input = ["First line\n", "Second line\n"]
      text = WikiText2(input)

      expect = [ Paragraph(ParagraphChunk, "First line Second line") ]
      TEST_EQ(expect, text.makeParas())


   def testRenderParagraphBreak(self):
      input = (
"""First paragraph

Second paragraph
""").splitlines()

      text = WikiText2(input)

      expect = [
         Paragraph(ParagraphChunk, "First paragraph"),
         Paragraph(ParagraphChunk, "Second paragraph"),
      ]
      TEST_EQ(expect, text.makeParas())


   def testHeading1(self):
      input = "= Heading =\nsome text\n".splitlines()
      text = WikiText2(input)

      expect = [
         Paragraph(Heading1Chunk, "Heading"),
         Paragraph(ParagraphChunk, "some text")
      ]
      TEST_EQ(expect, text.makeParas())


   def testHeading2(self):
      input = "== Heading ==\nsome text\n".splitlines()
      text = WikiText2(input)

      expect = [
         Paragraph(Heading2Chunk, "Heading"),
         Paragraph(ParagraphChunk, "some text")
      ]
      TEST_EQ(expect, text.makeParas())


   def testHeading3(self):
      input = "=== Heading ===\nsome text\n".splitlines()
      text = WikiText2(input)

      expect = [
         Paragraph(Heading3Chunk, "Heading"),
         Paragraph(ParagraphChunk, "some text")
      ]
      TEST_EQ(expect, text.makeParas())


   def testHeading4(self):
      input = "==== Heading ====\nsome text\n".splitlines()
      text = WikiText2(input)

      expect = [
         Paragraph(Heading4Chunk, "Heading"),
         Paragraph(ParagraphChunk, "some text")
      ]
      TEST_EQ(expect, text.makeParas())


   def testHeading5(self):
      input = "===== Heading =====\nsome text\n".splitlines()
      text = WikiText2(input)

      expect = [
         Paragraph(Heading5Chunk, "Heading"),
         Paragraph(ParagraphChunk, "some text")
      ]
      TEST_EQ(expect, text.makeParas())


   def testLinkInHeading(self):
      input = "= [[Page That Exists]] =\n".splitlines()
      text = WikiText2(input, WikiRepository("TESTWIKI"))

      expect = [
         Paragraph(
            Heading1Chunk,
            '<A HREF="http://greenlightwiki.com/Page_That_Exists">Page That Exists</A>'
         )
      ]
      TEST_EQ(expect, text.makeParas())


   def testEqualsSignInHeading(self):
      input = "===== 2 + 2 = 4 =====\n".splitlines()
      text = WikiText2(input)

      expect = [
         Paragraph(
            Heading5Chunk,
            '2 + 2 = 4'
         )
      ]
      TEST_EQ(expect, text.makeParas())


   def testForceLineBreak(self):
      input = "First line\n Second line\n".splitlines()
      text = WikiText2(input)

      expect = [
         Paragraph(ParagraphChunk, "First line<br>Second line")
      ]
      TEST_EQ(expect, text.makeParas())


   def testForceLineBreakSpecialExceptions(self):
      input = [
         " First line\n",
         " Second line\n",
         "\n",
         " Fourth\n",
         " Fifth\n",
      ]
      text = WikiText2(input)

      expect = [
         Paragraph(ParagraphChunk, "First line<br>Second line"),
         Paragraph(ParagraphChunk, "Fourth<br>Fifth"),
      ]
      TEST_EQ(expect, text.makeParas())


   def testBulletedListItem(self):
      input = ["* item [[With Link]]\n"]
      text = WikiText2(input, WikiRepository("TESTWIKI"))

      expect = [
         Paragraph(UnorderedListItemChunk, 'item <A HREF="http://greenlightwiki.com/With_Link" CLASS="new">With Link</A>')
      ]
      TEST_EQ(expect, text.makeParas())


   def testTwoBulletedListItems(self):
      input = [
         "* item [[With Link]]\n",
         "* second item\n",
      ]
      text = WikiText2(input, WikiRepository("TESTWIKI"))

      expect = [
         Paragraph(UnorderedListItemChunk, 'item <A HREF="http://greenlightwiki.com/With_Link" CLASS="new">With Link</A>'),
         Paragraph(UnorderedListItemChunk, "second item")
      ]
      TEST_EQ(expect, text.makeParas())


   def testNumberedList(self):
      input = \
"""# first item
#  item [[With Link]]

# third item
""".splitlines()

      text = WikiText2(input, WikiRepository("TESTWIKI"))

      expect = [
         Paragraph(OrderedListItemChunk, "first item"),
         Paragraph(OrderedListItemChunk, 'item <A HREF="http://greenlightwiki.com/With_Link" CLASS="new">With Link</A>'),
         Paragraph(OrderedListItemChunk, "third item"),
      ]
      TEST_EQ(expect, text.makeParas())


   def testTwoNumberedLists(self):
      input = \
"""# first item
# second item

# third item
some text

not in a list
# first new item

# second new item
""".splitlines()

      text = WikiText2(input)

      expect = [
         Paragraph(OrderedListItemChunk, "first item"),
         Paragraph(OrderedListItemChunk, "second item"),
         Paragraph(OrderedListItemChunk, "third item some text"),
         Paragraph(ParagraphChunk, "not in a list"),
         Paragraph(OrderedListItemChunk, "first new item"),
         Paragraph(OrderedListItemChunk, "second new item"),
      ]
      #TODO: verify that the numbers come out right
      TEST_EQ(expect, text.makeParas())


#    def testArbitraryHtmlElementInsideAParagraph(self):
#       input = [
#          Span("date", "(July 1, 56 B.C.)"),
#          "Some text"
#       ]
# 
#       text = WikiText2(input)
# 
#       expect = '<P><SPAN CLASS="date">(July 1, 56 B.C.)</SPAN>Some text</P>\n'
# 
#       TEST_EQ(expect, text.renderHtml())
# 
#       
#    def teestRecentChanges(self):
#       self._setUpRecentChanges()
# 
#       input = ["{{RecentChanges}}\n"]
#       text = WikiText2(input, testRepository)
# 
#       expect = RecentChanges.render(testRepository.recentChangesFilename())
# 
#       TEST_EQ(expect, [ text.replaceWords(line) for line in input ])
# 
# 
#    def _setUpRecentChanges(self):
#       utMisc.forceRemove("TESTDATA.RecentChanges")
# 
#       command = WikiCommand(
#          "SAVE",
#          "TESTDATA",
#          "PageTitle",
#          None,
#          "MrUser",
#       )
# 
#       RecentChanges.logChange(command)
# 
#       command = WikiCommand(
#          "SAVE",
#          "TESTDATA",
#          "OtherPage",
#          None,
#          "GeorgeGibbons",
#       )
# 
#       RecentChanges.logChange(command)
# 
# 
#    def teestRenderHtmlBody(self):
#       input = ["{{htmlTest.html}}"]
#       text = WikiText2(input)
# 
#       expect = """
#    Some body text begins here&#150;with an ampersand: &amp;.
#    <P>
#    Some more body <A HREF="http://nothing.com">text</A>.
# """
#       TEST_EQ([expect], text.renderParas())
# 
# 
#    def teestOnlyGetFromSafeDirectory(self):
#       input = ["{{../unauthorized/htmlTest.html}}"]
#       text = WikiText2(input)
# 
#       expect = """
#    Some body text begins here&#150;with an ampersand: &amp;.
#    <P>
#    Some more body <A HREF="http://nothing.com">text</A>.
# """
#       TEST_EQ([expect], text.renderParas())
# 
# 
#    # TODO: render non-existent html file
# 
# 
   def testHorizontalRule(self):
      input = "---\n----\n----   \n---- After a rule\n".splitlines()
      text = WikiText2(input)

      expect = [
         Paragraph(ParagraphChunk, "---"),
         Paragraph(ParagraphChunk, "<HR>"),
         Paragraph(ParagraphChunk, "<HR>"),
         Paragraph(ParagraphChunk, "<HR> After a rule")
      ]
      TEST_EQ(expect, text.makeParas())

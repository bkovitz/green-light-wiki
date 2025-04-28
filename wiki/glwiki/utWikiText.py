from teest import *
from os.path import normpath
import RecentChanges, utMisc
from WikiCommand import WikiCommand
from WikiRepository import WikiRepository, NullRepository
from LatexImage import LatexImage

from WikiText import WikiText, WordReplacer, bullet
from Html import ListRow, HtmlAnchor, Span
from UnsmashWords import unsmashWords

testRepository = NullRepository()
testRepository.recentChangesFilename = lambda: "TESTDATA.RecentChanges"


class ut_WikiText:

   def testSimpleRender(self):
      input = ["First line\n", "Second line\n"]
      text = WikiText(input)

      expect = \
"""<P>First line
Second line</P>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testRenderParagraphBreak(self):
      input = (
"""First paragraph

Second paragraph
""").splitlines()

      text = WikiText(input)

      expect = \
"""<P>First paragraph</P>
<P>Second paragraph</P>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testHorizontalRule(self):
      input = "---\n----\n----   \n---------- After the rule\n".splitlines()
      text = WikiText(input)

      expect = \
"""<P>---</P>
<HR>
<HR>
<HR>
<P>After the rule</P>
"""
 
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testHeading1(self):
      input = "= Heading =\nsome text\n".splitlines()
      text = WikiText(input)

      expect = \
"""<H1>Heading</H1>
<P>some text</P>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testHeading2(self):
      input = "== Heading ==\nsome text\n".splitlines()
      text = WikiText(input)

      expect = \
"""<H2>Heading</H2>
<P>some text</P>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testHeading3(self):
      input = "=== Heading ===\nsome text\n".splitlines()
      text = WikiText(input)

      expect = \
"""<H3>Heading</H3>
<P>some text</P>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testHeading4(self):
      input = "==== Heading ====\nsome text\n".splitlines()
      text = WikiText(input)

      expect = \
"""<H4>Heading</H4>
<P>some text</P>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testHeading5(self):
      input = "===== Heading =====\nsome text\n".splitlines()
      text = WikiText(input)

      expect = \
"""<H5>Heading</H5>
<P>some text</P>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testLinkInHeading(self):
      input = "= [[Page That Exists]] =\n".splitlines()
      text = WikiText(input, WikiRepository("TESTWIKI"))

      expect = \
"""<H1><A HREF="http://greenlightwiki.com/Page_That_Exists">Page That Exists</A></H1>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testEqualsSignInHeading(self):
      input = "===== 2 + 2 = 4 =====\n".splitlines()
      text = WikiText(input)

      expect = \
"""<H5>2 + 2 = 4</H5>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testForceLineBreak(self):
      input = "First line\n Second line\n".splitlines()
      text = WikiText(input)

      expect = \
"""<P>First line
<BR>
Second line</P>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testForceLineBreakSpecialExceptions(self):
      input = [
         " First line\n",
         " Second line\n",
         "\n",
         " Fourth\n",
         " Fifth\n",
      ]
      text = WikiText(input)

      expect = \
"""<P>First line
<BR>
Second line</P>
<P>Fourth
<BR>
Fifth</P>
"""
      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testHtmlSpecialChars(self):
      input = "< > &\n<this> &that\n<<<>>>&&&\n".splitlines()
      replacer = WordReplacer()

      expect = [
         "&lt; &gt; &amp;",
         "&lt;this&gt; &amp;that",
         "&lt;&lt;&lt;&gt;&gt;&gt;&amp;&amp;&amp;"
      ]
      TEST_EQ(expect, [ replacer.replaceWords(line) for line in input ])


   def testHttp(self):
      input = [
         "http://some_url.html\n",
         "http://with-period.htm.\n",
         "http://with-slash/\n",
         "[[Google http://google.com]]\n",
         "[[http://google.com Google]]\n",
         "http://some_url/image.gif.\n",
      ]
      replacer = WordReplacer()

      expect = [
         '<A HREF="http://some_url.html" CLASS="external">http://some_url.html</A>',
         '<A HREF="http://with-period.htm" CLASS="external">http://with-period.htm</A>.',
         '<A HREF="http://with-slash/" CLASS="external">http://with-slash/</A>',
         '<A HREF="http://google.com" CLASS="external">Google</A>',
         '<A HREF="http://google.com" CLASS="external">Google</A>',
         '<IMG SRC="http://some_url/image.gif" BORDER=0>.',
      ]
      TEST_EQ(expect, [ replacer.replaceWords(line) for line in input ])


   def testFtp(self):
      input = [
         "ftp://some_url.html\n",
         "ftp://with-period.htm.\n",
         "ftp://with-slash/\n",
         "[[Google ftp://google.com]]\n",
         "[[ftp://google.com Google]]\n",
         "ftp://some_url/image.gif.\n",
      ]
      replacer = WordReplacer()

      expect = [
         '<A HREF="ftp://some_url.html" CLASS="external">ftp://some_url.html</A>',
         '<A HREF="ftp://with-period.htm" CLASS="external">ftp://with-period.htm</A>.',
         '<A HREF="ftp://with-slash/" CLASS="external">ftp://with-slash/</A>',
         '<A HREF="ftp://google.com" CLASS="external">Google</A>',
         '<A HREF="ftp://google.com" CLASS="external">Google</A>',
         '<IMG SRC="ftp://some_url/image.gif" BORDER=0>.',
      ]
      TEST_EQ(expect, [ replacer.replaceWords(line) for line in input ])


   def testHttps(self):
      input = [
         "https://some_url.html\n",
         "https://with-period.htm.\n",
         "https://with-slash/\n",
         "[[Google https://google.com]]\n",
         "[[https://google.com Google]]\n",
         "https://some_url/image.gif.\n",
      ]
      replacer = WordReplacer()

      expect = [
         '<A HREF="https://some_url.html" CLASS="external">https://some_url.html</A>',
         '<A HREF="https://with-period.htm" CLASS="external">https://with-period.htm</A>.',
         '<A HREF="https://with-slash/" CLASS="external">https://with-slash/</A>',
         '<A HREF="https://google.com" CLASS="external">Google</A>',
         '<A HREF="https://google.com" CLASS="external">Google</A>',
         '<IMG SRC="https://some_url/image.gif" BORDER=0>.',
      ]
      TEST_EQ(expect, [ replacer.replaceWords(line) for line in input ])


   def testMailto(self):
      input = "mailto:someone@there.com\nmailto:period.com.\n".splitlines()
      replacer = WordReplacer()

      expect = [
         '<A HREF="mailto:someone@there.com" CLASS="external">mailto:someone@there.com</A>',
         '<A HREF="mailto:period.com" CLASS="external">mailto:period.com</A>.',
      ]
      TEST_EQ(expect, [ replacer.replaceWords(line) for line in input ])


   def testBracketLink(self):
      input = "[[word]]\n[[two words]]\n[[Apostrophe'd Word]]".splitlines()
      replacer = WordReplacer(WikiRepository("TESTWIKI"))

      expect = [
         '<A HREF="http://greenlightwiki.com/word" CLASS="new">word</A>',
         '<A HREF="http://greenlightwiki.com/two_words" CLASS="new">two words</A>',
         '<A HREF="http://greenlightwiki.com/Apostrophe%27d_Word" CLASS="new">Apostrophe\'d Word</A>',
      ]
      TEST_EQ(expect, [ replacer.replaceWords(line) for line in input ])


   def testLinkToExistingPage(self):
      input = "PageThatExists\n[[Page That Exists]]\n".splitlines()
      replacer = WordReplacer(WikiRepository("TESTWIKI"))

      expect = [
         'PageThatExists', # no more WikiWords!
         '<A HREF="http://greenlightwiki.com/Page_That_Exists">Page That Exists</A>', ]
      TEST_EQ(expect, [ replacer.replaceWords(line) for line in input ])


   def testSimpleItalics(self):
      input = [
         "One ''word'' in italics\n",
         "Italics at end of ''line:''\n",
         "Next line, with no italics\n",
      ]
      replacer = WordReplacer()

      expect = [
         "One <EM>word</EM> in italics",
         "Italics at end of <EM>line:</EM>",
         "Next line, with no italics",
      ]
      TEST_EQ(expect, [ replacer.replaceWords(line) for line in input ])


   def testSimpleBold(self):
      input = ["One '''word''' in bold"]
      replacer = WordReplacer()

      expect = ["One <STRONG>word</STRONG> in bold"]
      TEST_EQ(expect, [ replacer.replaceWords(line) for line in input ])


   def testBulletedListItem(self):
      input = ["* item [[With Link]]\n"]
      text = WikiText(input, WikiRepository("TESTWIKI"))

      expect = \
"""<UL>
  <LI>item <A HREF="http://greenlightwiki.com/With_Link" CLASS="new">With Link</A></LI>
</UL>
"""
      TEST_EQ(expect, str(text.renderParas()[0]))


   def testTwoBulletedListItems(self):
      input = [
         "* item [[With Link]]\n",
         "* second item\n",
      ]
      text = WikiText(input, WikiRepository("TESTWIKI"))

      expect = \
"""<UL>
  <LI>item <A HREF="http://greenlightwiki.com/With_Link" CLASS="new">With Link</A></LI>
  <LI>second item</LI>
</UL>
"""
      TEST_EQ(expect, str(text.renderParas()[0]))


   def testNumberedList(self):
      input = \
"""# first item
#  item [[With Link]]

# third item
""".splitlines()

      text = WikiText(input, WikiRepository("TESTWIKI"))

      expect = \
"""<OL>
  <LI>first item</LI>
  <LI>item <A HREF="http://greenlightwiki.com/With_Link" CLASS="new">With Link</A></LI>
  <LI>third item</LI>
</OL>
"""

      TEST_EQ(expect, str(text.renderParas()[0]))


   def testTwoNumberedLists(self):
      input = \
"""# first item
# second item

# third item
some text
# first new item

# second new item
""".splitlines()

      text = WikiText(input)

      expect = \
"""<OL>
  <LI>first item</LI>
  <LI>second item</LI>
  <LI>third item</LI>
</OL>
<P>some text</P>
<OL>
  <LI>first new item</LI>
  <LI>second new item</LI>
</OL>
"""

      TEST_EQ(expect, "".join([str(para) for para in text.renderParas()]))


   def testArbitraryHtmlElementInsideAParagraph(self):
      input = [
         Span("date", "(July 1, 56 B.C.)"),
         "Some text"
      ]

      text = WikiText(input)

      expect = '<P><SPAN CLASS="date">(July 1, 56 B.C.)</SPAN>Some text</P>\n'

      TEST_EQ(expect, text.renderHtml())

      
   def teestRecentChanges(self):
      self._setUpRecentChanges()

      input = ["{{RecentChanges}}\n"]
      text = WikiText(input, testRepository)

      expect = RecentChanges.render(testRepository.recentChangesFilename())

      TEST_EQ(expect, [ text.replaceWords(line) for line in input ])


   def _setUpRecentChanges(self):
      utMisc.forceRemove("TESTDATA.RecentChanges")

      command = WikiCommand(
         "SAVE",
         "TESTDATA",
         "PageTitle",
         None,
         "MrUser",
      )

      RecentChanges.logChange(command)

      command = WikiCommand(
         "SAVE",
         "TESTDATA",
         "OtherPage",
         None,
         "GeorgeGibbons",
      )

      RecentChanges.logChange(command)


   def testUnsmashWords(self):
      TEST_EQ("One Two", unsmashWords("OneTwo"))
      TEST_EQ("One Two", unsmashWords("One_Two"))
      TEST_EQ("One about Two", unsmashWords("One_about_Two"))
      TEST_EQ("Lev 1 lev 2", unsmashWords("Lev_1_lev_2"))
      TEST_EQ("OneTwo", unsmashWords("OneTwo_"))
      TEST_EQ("djkfhdjsfhjkdhf", unsmashWords("djkfhdjsfhjkdhf"))


   def teestRenderHtmlBody(self):
      input = ["{{htmlTest.html}}"]
      text = WikiText(input)

      expect = """
   Some body text begins here&#150;with an ampersand: &amp;.
   <P>
   Some more body <A HREF="http://nothing.com">text</A>.
"""
      TEST_EQ([expect], text.renderParas())


   def teestOnlyGetFromSafeDirectory(self):
      input = ["{{../unauthorized/htmlTest.html}}"]
      text = WikiText(input)

      expect = """
   Some body text begins here&#150;with an ampersand: &amp;.
   <P>
   Some more body <A HREF="http://nothing.com">text</A>.
"""
      TEST_EQ([expect], text.renderParas())


   # TODO: render non-existent html file


   def testParseLatex(self):
      replacer = WordReplacer()
      expect = [r"$$\int_a^b e^{it}f(t)\,dt$$"]
      got = replacer.allWords("$$\int_a^b e^{it}f(t)\,dt$$")
      TEST_EQ(expect, got)


   def testTwoLatexStringsOnOneLine(self):
      replacer = WordReplacer()
      expect = [
         "Variable",
         " ",
         "$$a$$",
         " ",
         "and",
         " ",
         "variable",
         " ",
         "$$b$$",
         "."
      ]
      got = replacer.allWords("Variable $$a$$ and variable $$b$$.")
      TEST_EQ(expect, got)


   def testLatexImage(self):
      input = r"$$\int_a^b e^{it}f(t)\,dt$$"
      replacer = WordReplacer(WikiRepository("TESTWIKI"))

      got = replacer.replaceWordsWithObjects(input)

      TEST_EQ(1, len(got))
      TEST_EQ(LatexImage, got[0].__class__)

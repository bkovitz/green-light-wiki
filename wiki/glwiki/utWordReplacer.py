from teest import *

from WordReplacer import WordReplacer
from WikiRepository import WikiRepository, NullRepository
from LatexImage import LatexImage

class ut_WordReplacer:

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

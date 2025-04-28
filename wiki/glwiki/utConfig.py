from teest import *
import sys

from Config import Config
from StringIO import StringIO

class ut_Config:

   def testOneItem(self):
      fakeFile = StringIO("wiki-directory:./righthere\n")
      config = Config(fakeFile)

      TEST_EQ(config.get("", "wiki-directory"), "./righthere")
      TEST_EQ(config.get("", "undefined"), "")


   def testSpaces(self):
      fakeFile = StringIO(" wiki name\t : This Here Wiki  \n")
      config = Config(fakeFile)

      TEST_EQ(config.get("", "wiki name"), "This Here Wiki")


   def testColonInValue(self):
      fakeFile = StringIO("some name: Blah:Blah\n")
      config = Config(fakeFile)

      TEST_EQ(config.get("", "some name"), "Blah:Blah")


   def testEmptyValue(self):
      fakeFile = StringIO("nothing:\n")
      config = Config(fakeFile)

      TEST_EQ(config.get("", "nothing"), "")


   def testBlanksAndComments(self):
      fakeFile = StringIO("# comment\n   #   comment  \nname: value\n")
      config = Config(fakeFile)

      TEST_EQ(config.get("", "name"), "value")


   def testMakeUrl(self):
      fakeFile = StringIO("url prefix: http://prefix.com?\n")
      config = Config(fakeFile)

      TEST_EQ(config.makeUrl("", "PageName"), "http://prefix.com?PageName")


   def testWikiSpecificConfig(self):
      fakeFile = StringIO("""
wiki executable: /cgi-bin/wiki.cgi

WIKI testWiki
url prefix:   http://glwiki.com/testWiki/
logo file:    /giraffe-logo.gif

WIKI other-wiki
url prefix:   http://glwiki.com/other-wiki/
logo file:    /other-logo.gif
""")
      config = Config(fakeFile)

      TEST_EQ(config.get("testWiki", "wiki executable"), "/cgi-bin/wiki.cgi")
      TEST_EQ(config.get("testWiki", "url prefix"), "http://glwiki.com/testWiki/")
      TEST_EQ(config.get("other-wiki", "url prefix"), "http://glwiki.com/other-wiki/")
      

   def testGetNonwikiFilename(self):
      fakeFile = StringIO("""
base directory: /var/www/html
""")
      config = Config(fakeFile)

      TEST_EQ(
         "/var/www/html/index.html",
         config.getNonwikiFilename("index.html")
      )


   def testGetNonwikiFilenameWithTrailingSlash(self):
      fakeFile = StringIO("""
base directory: /var/www/html/
""")
      config = Config(fakeFile)

      TEST_EQ(
         "/var/www/html/index.html",
         config.getNonwikiFilename("index.html")
      )


   def testGetNonwikiFilenameWithLeadingSlash(self):
      fakeFile = StringIO("""
base directory: /var/www/html
""")
      config = Config(fakeFile)

      TEST_EQ(
         "/var/www/html/index.html",
         config.getNonwikiFilename("/index.html")
      )


   def testGetNonwikiFilenameWithNoBaseDefined(self):
      fakeFile = StringIO()
      config = Config(fakeFile)

      TEST_EQ(
         "index.html",
         config.getNonwikiFilename("index.html")
      )


   def testIsYes(self):
      fakeFile = StringIO(
"""login to edit:  yes
other flag:        yep
another:           y
a no flag:         no
""")
      config = Config(fakeFile)

      TEST(config.isYes("", "login to edit"))
      TEST(config.isYes("NonexistentWiki", "login to edit"))
      TEST(config.isYes("", "other flag"))
      TEST(config.isYes("", "another"))
      TEST(not config.isYes("", "a no flag"))
      TEST(not config.isYes("", "undefined flag"))

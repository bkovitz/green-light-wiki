from teest import *

from WikiCommand import WikiCommand, makeWikiCommandFromApacheEnvironment, \
                        getWikiNameFromApacheEnvironment, \
                        getPageNameFromApacheEnvironment
from WikiCommand import _extractPageName, _extractWikiName

from io import StringIO

class ut_WikiCommand:

   def testGetWikiName(self):
      environ = {
         "REDIRECT_URL": "/heuristic/YawningVoid",
         "REQUEST_METHOD": "GET",
      }

      wikiName = getWikiNameFromApacheEnvironment(environ)

      TEST_EQ("heuristic", wikiName)


   def testGetPageName(self):
      environ = {
         "REDIRECT_URL": "/heuristic/YawningVoid",
         "REQUEST_METHOD": "GET",
      }

      pageName = getPageNameFromApacheEnvironment(environ)

      TEST_EQ("YawningVoid", pageName)


   def testDisplay(self):
      environ = {
         "REDIRECT_URL": "/heuristic/YawningVoid",
         "REQUEST_METHOD": "GET",
      }

      command = makeWikiCommandFromApacheEnvironment(environ)

      TEST_EQ("heuristic", command.wikiName)
      TEST_EQ("YawningVoid", command.pageName)
      TEST_EQ("DISPLAY", command.command)


   def testEdit(self):
      environ = {
         "REDIRECT_URL": "/fakeWiki/fakePage",
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "action=edit"
      }

      command = makeWikiCommandFromApacheEnvironment(environ)

      TEST_EQ("fakeWiki", command.wikiName)
      TEST_EQ("fakePage", command.pageName)
      TEST_EQ("EDIT", command.command)


   def testSave(self):
      environ = {
         "REDIRECT_URL": "/WikiTitle/PageTitle",
         "REQUEST_METHOD": "POST",
      }
      fakeStdin = StringIO(
         "origVersion=2%0D%0A\ntext=First+line%0D%0ASecond+line%0D%0A\n"
      )

      command = makeWikiCommandFromApacheEnvironment(environ, fakeStdin)

      TEST_EQ("SAVE", command.command)
      TEST_EQ("WikiTitle", command.wikiName)
      TEST_EQ("PageTitle", command.pageName)
      TEST_EQ(2, int(command.formDict["origVersion"]))
      expect = ["First line\r\n", "Second line\r\n"]
      TEST_EQ(command.inputFile.readlines(), expect)


   def testForceWikiName(self):
      environ = {
         "REDIRECT_URL": "/big-site/wiki/YawningVoid",
         "REQUEST_METHOD": "GET",
      }

      command = makeWikiCommandFromApacheEnvironment(
         environ, stdin=None, wikiName="forcedWiki"
      )

      TEST_EQ("forcedWiki", command.wikiName)
      TEST_EQ("YawningVoid", command.pageName)
      TEST_EQ("DISPLAY", command.command)


   def testForceWikiNameWithDefaultPage(self):
      environ = {
         "REDIRECT_URL": "/big-site/wiki/",
         "REQUEST_METHOD": "GET",
      }

      command = makeWikiCommandFromApacheEnvironment(
         environ, stdin=None, wikiName="forcedWiki"
      )

      TEST_EQ("forcedWiki", command.wikiName)
      TEST_EQ("", command.pageName)
      TEST_EQ("DISPLAY", command.command)


   def testGetHtml(self):
      environ = {
         "REDIRECT_URL": "/heuristic/YawningVoid.html",
         "REQUEST_METHOD": "GET",
      }

      command = makeWikiCommandFromApacheEnvironment(environ)

      TEST_EQ("heuristic", command.wikiName)
      TEST_EQ("YawningVoid.html", command.pageName)
      TEST_EQ("STATIC", command.command)


   # URL-parsing -------------------------------------------------------

   def testNormalCase(self):
      path = "/wiki_name/PageName"

      TEST_EQ("wiki_name", _extractWikiName(path))
      TEST_EQ("PageName", _extractPageName(path))


   def testFullUrl(self):
      path = "http://wiki_name/PageName"

      TEST_EQ("wiki_name", _extractWikiName(path))
      TEST_EQ("PageName", _extractPageName(path))


   def testNoPageName(self):
      path = "/wiki_name/"

      TEST_EQ("wiki_name", _extractWikiName(path))
      TEST_EQ("", _extractPageName(path))


   def testNoPageNameNoTerminatingSlash(self):
      path = "/wiki_name"

      TEST_EQ("wiki_name", _extractWikiName(path))
      TEST_EQ("", _extractPageName(path))


   def testNoPageNameNoSlashesAtAll(self):
      path = "wiki_name"

      TEST_EQ("wiki_name", _extractWikiName(path))
      TEST_EQ("", _extractPageName(path))


   def testEmptyString(self):
      path = ""

      TEST_EQ("", _extractWikiName(path))
      TEST_EQ("", _extractPageName(path))


   # miscellaneous -----------------------------------------------------

   def testEquality(self):
      c1 = WikiCommand("DISPLAY", "fakeWiki", "fakePageName")
      c2 = WikiCommand("DISPLAY", "fakeWiki", "fakePageName")

      TEST_EQ(c1, c2)


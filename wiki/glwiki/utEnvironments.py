from teest import *

from Environments import getEnvironment, ApacheEnvironment, _extractSessionId
from BadPage import BadPage
from StaticPage import StaticPage
from CommandLine import CommandLine
from utMisc import NonexistentFile, FileFromList
from Misc import forceRemove
from io import StringIO
from time import time
# from Cookie import SimpleCookie
from http.cookies import SimpleCookie

from PlainPage import PlainPage
from DisplayPage import DisplayPage
from EditNewPage import EditNewPage
from EditPage import EditPage
from DisplayRecentChanges import DisplayRecentChanges
from DisplayAllPages import DisplayAllPages
from VersionHistoryPage import VersionHistoryPage
import SessionDatabase

class ut_Environments:

   def setUp(self):
      forceRemove("wiki.sessions")


   def testGetApache(self):
      now = 1065053273
      sessionId = SessionDatabase.makeSession(
         time(),
         "128.129.130.131",
      )

      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "",
         "REQUEST_URI": "testWiki/Welcome_Page",
         "REMOTE_ADDR": "128.129.130.131",
         'HTTP_COOKIE': '$Version="1"; wiki-session="%s"; $Path="/ben"; $Domain=".cds.caltech.edu", $Version="1"; other-cookie="blah blah blah"; $Path="/ben"; $Domain=".cds.caltech.edu"' % sessionId
      }
      stdin = StringIO()

      got = getEnvironment(cmdArgs, environ, NonexistentFile(), stdin)

      TEST_EQ(ApacheEnvironment, got.__class__)
      TEST_EQ("GET", got.getRequest())
      TEST_EQ({}, got.getQueryDict())
      TEST_EQ("testWiki/Welcome_Page", got.getUri())
      TEST_EQ(sessionId, got.getSessionId())


   def testApacheNoCookie(self):
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "",
         "REQUEST_URI": "testWiki/Welcome_Page",
         "REMOTE_ADDR": "128.129.130.131",
      }
      stdin = StringIO()

      got = getEnvironment(cmdArgs, environ, NonexistentFile(), stdin)

      TEST_EQ("128.129.130.131", got.getUserName())


   def testGetBadPage(self):
      wikiDirs = FileFromList([
         "wiki/*"
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "",
         "REQUEST_URI": "non-existent.html"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      got = env.getRequestedPage()

      TEST_EQ(BadPage, got.__class__)


   def testGetStaticPage(self):
      wikiDirs = FileFromList([
         "WIKI wiki/*",
         "STATIC TESTSTATIC/*.html",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "",
         "REQUEST_URI": "TESTSTATIC/htmlTest.html"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      got = env.getRequestedPage()

      TEST_EQ(StaticPage, got.__class__)


   def testGetPlainPage(self):
      wikiDirs = FileFromList([
         "WIKI wiki/*",
         "PLAIN TESTPLAIN/*.html",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "",
         "REQUEST_URI": "TESTPLAIN/htmlTest.html"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      got = env.getRequestedPage()

      TEST_EQ(PlainPage, got.__class__)


   def testGetDisplayPage(self):
      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
         "STATIC *.html",
         "PLAIN *.htm",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "",
         "REQUEST_URI": "TESTWIKI/PageThatExists"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      got = env.getRequestedPage()

      TEST_EQ(DisplayPage, got.__class__)
      TEST_EQ("TESTWIKI", got._repository.getWikiName())
      TEST_EQ("PageThatExists", got.getPageName())


   def testGetDefaultPage(self):
      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
         "STATIC *.html",
         "PLAIN *.htm",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "",
         "REQUEST_URI": "TESTWIKI"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      got = env.getRequestedPage()

      TEST_EQ("WelcomePage", got.getPageName())
      TEST_EQ(DisplayPage, got.__class__)
      TEST_EQ("TESTWIKI", got._repository.getWikiName())


   def testGetEditNewPage(self):
      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
         "STATIC *.html",
         "PLAIN *.htm",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "",
         "REQUEST_URI": "TESTWIKI/NonexistentPage"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      got = env.getRequestedPage()

      TEST_EQ(EditNewPage, got.__class__)
      TEST_EQ("TESTWIKI", got._repository.getWikiName())
      TEST_EQ("NonexistentPage", got.getPageName())


   def testGetEditPage(self):
      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
         "STATIC *.html",
         "PLAIN *.htm",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "action=edit",
         "REQUEST_URI": "TESTWIKI/PageThatExists?action=edit"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      got = env.getRequestedPage()

      TEST_EQ(EditPage, got.__class__)
      TEST_EQ("TESTWIKI", got._repository.getWikiName())
      TEST_EQ("PageThatExists", got.getPageName())


   def testGetVersionHistoryPage(self):
      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "action=history",
         "REQUEST_URI": "TESTWIKI/PageThatExists?action=history"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      got = env.getRequestedPage()

      TEST_EQ(VersionHistoryPage, got.__class__)
      TEST_EQ("TESTWIKI", got._repository.getWikiName())
      TEST_EQ("PageThatExists", got.getPageName())


   def testGetRecentChanges(self):
      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
         "STATIC *.html",
         "PLAIN *.htm",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "action=edit",
         "REQUEST_URI": "TESTWIKI/RecentChanges"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      got = env.getRequestedPage()

      TEST_EQ(DisplayRecentChanges, got.__class__)
      TEST_EQ("TESTWIKI", got._repository.getWikiName())


   def testGetAllPages(self):
      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
         "STATIC *.html",
         "PLAIN *.htm",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "action=edit",
         "REQUEST_URI": "TESTWIKI/AllPages"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      got = env.getRequestedPage()

      TEST_EQ(DisplayAllPages, got.__class__)
      TEST_EQ("TESTWIKI", got._repository.getWikiName())


   def testGetPageWithSpacesInTheName(self):
      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
         "STATIC *.html",
         "PLAIN *.htm",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "action=edit",
         "REQUEST_URI": "TESTWIKI/A%20Name%20with%20spaces"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)

      TEST_EQ("TESTWIKI/A Name with spaces", env.getPageName())


   def testGetPageWithQuestionMark(self):
      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
         "STATIC *.html",
         "PLAIN *.htm",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "action=edit",
         "REQUEST_URI": "TESTWIKI/What_is_a_wiki%3F"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)

      TEST_EQ("TESTWIKI/What_is_a_wiki?", env.getPageName())


   def testIgnoreSpuriousComma(self):
      """test workaround for bug in Cookie's parsing routine"""

      cookie = SimpleCookie()
      cookie.load('$Version="1"; wiki-session=fKoeAgK2N14qV6z9l7s3, SITESERVER=ID=07d36133d9879185cb3782bd2b275415, second_to_last_visit=1065127677, last_visit=1066157942, ad_browser_id=23135049')
      TEST_EQ("fKoeAgK2N14qV6z9l7s3", _extractSessionId(cookie))


   def testHttpHost(self):
      wikiDirs = FileFromList([
         "WIKI lenore-exegesis http://lenore-exegesis.com/*",
         "WIKI another-wiki http://another-wiki.com/*",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "GET",
         "QUERY_STRING": "action=edit",
         "HTTP_HOST": "another-wiki.com",
         "REQUEST_URI": "A_Page"
      }
      stdin = StringIO()

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)

      TEST_EQ("A_Page", env.getPageName())

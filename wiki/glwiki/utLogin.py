from teest import *
from utMisc import clearSessionDict, FileFromList, resetConfig

from StringIO import StringIO

from Login import Login
from Environments import getEnvironment
import SessionDatabase
from CommandLine import CommandLine
from DisplayPage import DisplayPage

class ut_Login:

   def setUp(self):
      clearSessionDict()
      resetConfig()


   def testLogin(self):
      now = 1065046739
      sessionId = SessionDatabase.makeSession(now, "128.129.130.131")

      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
         "STATIC *.html",
         "PLAIN *.htm",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "POST",
         "QUERY_STRING": "",
         "REQUEST_URI": "TESTWIKI/PageThatExists",
         "REMOTE_ADDR": "128.129.130.131",
         'HTTP_COOKIE': '$Version="1"; wiki-session="%s"; $Path="/ben"; $Domain=".cds.caltech.edu", $Version="1";' % sessionId
      }
      stdin = \
         StringIO("action=login&deferredAction=edit&userName=John+Mittens\n")

      assert not SessionDatabase.isLoggedIn(sessionId)

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      page = env.getRequestedPage()

      page.action()

      TEST(SessionDatabase.isLoggedIn(sessionId))
      TEST_EQ("John Mittens", SessionDatabase.getUserName(sessionId))

      output = page.cgiLeader()

      expect = \
"""Status: 303
Location: http://greenlightwiki.com/PageThatExists?action=edit
"""

      TEST_EQ(expect, output)

      page.renderCgi() # test that we don't crash
      page.getCommand()


   def testLoginWithUnknownSessionId(self):
      now = 1065046739
      sessionId = "FAKESESSIONID"

      wikiDirs = FileFromList([
         "WIKI TESTWIKI TESTWIKI/*",
         "STATIC *.html",
         "PLAIN *.htm",
      ])
      cmdArgs = CommandLine("Main.py".split())
      environ = {
         "REQUEST_METHOD": "POST",
         "QUERY_STRING": "",
         "REQUEST_URI": "TESTWIKI/PageThatExists",
         "REMOTE_ADDR": "128.129.130.131",
         'HTTP_COOKIE': '$Version="1"; wiki-session="%s"; $Path="/ben"; $Domain=".cds.caltech.edu", $Version="1";' % sessionId
      }
      stdin = \
         StringIO("action=login&deferredAction=edit&userName=John+Mittens\n")

      assert not SessionDatabase.isLoggedIn(sessionId)

      env = getEnvironment(cmdArgs, environ, wikiDirs, stdin)
      page = env.getRequestedPage()

      page.action()

      # newId = SessionDatabase.getSessionIdForUser("John Mittens")
      # TEST_NE(newId, sessionId)
      # TEST(SessionDatabase.isLoggedIn(newId))
      # TEST_EQ("John Mittens", SessionDatabase.getUserName(newId))

      output = page.cgiLeader()

      expect = ""
      '''
      expect = \
"""Status: 303
Location: http://greenlightwiki.com/PageThatExists?action=edit
Set-Cookie: wiki-session=%s; Domain=.greenlightwiki.com; Max-Age=15552000; Path=/; Version=1;
""" % newId
'''
      #TODO test with a regexp for newId?
      #TEST_EQ(expect, output)

      page.renderCgi() # test that we don't crash
      page.getCommand()



#TODO clear old username when it changes

#TODO deal with the fact that the same user can have sessions on multiple
# machines

#TODO respond to SAVE as deferred action

#TODO respond to DISP as deferred action

from teest import *
from utMisc import clearSessionDict

import os
import SessionDatabase
from SessionDatabase import BadSessionId
from Chunks import SuccessfulSaveChunk


class ut_SessionDatabase:

    def __init__(self):
        self.now = 1065046739

    def setUp(self):
        clearSessionDict()

    def tearDown(self):
        clearSessionDict()

    def testBasics(self):
        id = SessionDatabase.makeSession(self.now, "203.121.148.176")
        TEST(len(id) > 5)

        # TEST(SessionDatabase.sessionIdIsOk(id, "203.121.148.176"))
        # TEST(SessionDatabase.sessionIdIsOk(id, "203.121.148.185"))
        # TEST(not SessionDatabase.sessionIdIsOk(id, "203.121.145.176"))

        # TEST(not SessionDatabase.sessionIdIsOk("fake id", "203.121.148.176"))

        TEST_EQ("203.121.148.176", SessionDatabase.getUserName(id))

        SessionDatabase.setUserName(id, "George Gibbons")
        TEST_EQ("George Gibbons", SessionDatabase.getUserName(id))

        expect = (
            "Set-Cookie: wiki-session=%s; Domain=.greenlightwiki.com; Max-Age=15552000; Path=/; Version=1;"
            % id
        )
        TEST_EQ(expect, str(SessionDatabase.makeCookie(id)))

        """ TODO: verify persistence
      assert (
         os.access("wiki.sessions", os.F_OK)
         or
         os.access("wiki.sessions.db", os.F_OK)
      )
      """

    def testIsLoggedIn(self):
        id = SessionDatabase.makeSession(self.now, "128.129.130.131")

        TEST(not SessionDatabase.isLoggedIn(id))

        SessionDatabase.setUserName(id, "George Gibbons")

        TEST(SessionDatabase.isLoggedIn(id))

    def testDefaultIsNotLoggedIn(self):
        TEST(not SessionDatabase.isLoggedIn("FAKESESSIONID"))

    def testMakeNewSessionIdIfTheOneWeGotIsBad(self):
        TEST_EXC(
            BadSessionId,
            SessionDatabase.setUserName,
            "FAKESESSIONID",
            "Little George Gibbons",
        )

    def testPendingMessage(self):
        id = SessionDatabase.makeSession(self.now, "203.121.148.176")

        # no pending message yet
        TEST_EQ((None, None), SessionDatabase.getPendingMessage(id, self.now + 2))

        SessionDatabase.setPendingMessage(
            id, SuccessfulSaveChunk, "Page Title", self.now
        )

        # a pending message
        TEST_EQ(
            (SuccessfulSaveChunk, "Page Title"),
            SessionDatabase.getPendingMessage(id, self.now + 2),
        )

        # too late for pending message
        TEST_EQ((None, None), SessionDatabase.getPendingMessage(id, self.now + 11))

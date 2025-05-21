from teest import *
from utMisc import FakeEnvironment, forceRemove, resetConfig, clearSessionDict

from io import StringIO

from MightRequireLogin import MightRequireLogin
import SessionDatabase
from Config import config
from Html import HtmlPara

now = 1065202518


class ut_MightRequireLogin:

    def setUp(self):
        resetConfig()
        clearSessionDict()

    def testNotLoggedIn(self):
        config.readConfigFile(StringIO("login to edit: yes\n"))

        sessionId = SessionDatabase.makeSession(now, "128.129.130.131")

        env = FakeEnvironment(
            pathsList=["WIKI TESTWIKI/*"],
            requestMethod="GET",
            uri="/TESTWIKI/aPage",
            sessionId=sessionId,
        )

        page = MightRequireLogin(env)

        TEST(page.needLogin())

    def testLoggedIn(self):
        config.readConfigFile(StringIO("login to edit: yes\n"))

        sessionId = SessionDatabase.makeSession(now, "128.129.130.131")
        SessionDatabase.setUserName(sessionId, "George Gibbons")

        env = FakeEnvironment(
            pathsList=["WIKI TESTWIKI/*"],
            requestMethod="GET",
            uri="/TESTWIKI/aPage",
            sessionId=sessionId,
        )

        page = MightRequireLogin(env)

        TEST(not page.needLogin())

    def testNotLoggedInButConfigDoesntRequireLogins(self):
        config.readConfigFile(StringIO(""))

        sessionId = SessionDatabase.makeSession(now, "128.129.130.131")

        env = FakeEnvironment(
            pathsList=["WIKI TESTWIKI/*"],
            requestMethod="GET",
            uri="/TESTWIKI/aPage",
            sessionId=sessionId,
        )

        page = MightRequireLogin(env)

        TEST(not page.needLogin())

    def testLoginDiv(self):
        config.readConfigFile(
            StringIO(
                """login to edit: yes
default page:     Default_Page
url prefix:       http://greenlightwiki.com/testWiki/
"""
            )
        )

        env = FakeEnvironment(
            pathsList="WIKI testWiki/*",
            requestMethod="GET",
            uri="testWiki/aPage",
        )

        expect = """<DIV ID="wiki-message">
  <FORM ACTION="http://greenlightwiki.com/testWiki/aPage" METHOD=POST>
    <INPUT TYPE=HIDDEN NAME="action" VALUE="login"><INPUT TYPE=HIDDEN NAME="deferredAction" VALUE="edit"><P><A HREF="http://greenlightwiki.com/testWiki/Default_Page">Default Page</A></P>
    <H1>Log in</H1>
    <P>Message goes here.</P>
    <P>Enter your name:&nbsp;&nbsp;<INPUT TYPE=TEXT NAME="userName" SIZE="50" MAXLENGTH="100">&nbsp;&nbsp;<INPUT TYPE=SUBMIT VALUE=" Log in "></P>
    <P>Please enter your full name: first name and last name.  This will help people see which pages you've been working on when they click <A HREF="http://greenlightwiki.com/testWiki/Recent_Changes">Recent Changes</A>.</P>
    <P>If you'd prefer to edit anonymously, just leave the name field blank.</P>
    <P>Be sure to use spaces between the words in your name.</P>
  </FORM>
</DIV>
"""

        page = MightRequireLogin(env)

        got = page.genericLoginDiv("edit", HtmlPara("Message goes here."))

        TEST_EQ(expect, str(got))

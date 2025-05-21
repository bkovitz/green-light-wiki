from teest import *
from utMisc import FakeEnvironment
from io import StringIO

from EditNewPage import EditNewPage
from WikiRepository import WikiRepository
from Config import config
import SessionDatabase

from Html import (
    Html,
    HtmlMeta,
    HtmlForm,
    HtmlTextArea,
    HtmlInputSubmit,
    HtmlInputHidden,
)

now = 1065202518


class ut_EditNewPage:

    def testText(self):
        page = EditNewPage(
            FakeEnvironment(
                WikiRepository("TESTWIKI"), "NonexistentPage", "George Gibbons"
            )
        )

        expect = "Describe Nonexistent Page here."

        TEST_EQ(expect, page.text())

    def testEditDivWithLogin(self):
        # just a test to verify that we don't crash
        config.readConfigFile(StringIO("login to edit: yes\n"))
        sessionId = SessionDatabase.makeSession(now, "128.129.130.131")
        env = FakeEnvironment(
            pathsList=["WIKI TESTWIKI/*"],
            requestMethod="GET",
            uri="/TESTWIKI/aPage",
            sessionId=sessionId,
        )

        page = EditNewPage(env)

        TEST_EQ(str(page.contentDiv()), str(page.loginDiv()))

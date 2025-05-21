from teest import *
from utMisc import FakeEnvironment
from Misc import forceRemove

from DisplayAllPages import DisplayAllPages

import AllPages
from WikiRepository import WikiRepository
from Html import OneRowTable, ButtonLink


class ut_DisplayAllPages:

    def testAll(self):
        forceRemove("TESTWIKI/PageTitle")

        page = DisplayAllPages(
            FakeEnvironment(
                WikiRepository("TESTWIKI"), "TESTWIKI/AllPages", "George Gibbons"
            )
        )

        expect = [
            '<P CLASS="item"><A HREF="http://greenlightwiki.com/PageThatExists">Page That Exists</A></P>\n',
            '<P CLASS="item"><A HREF="http://greenlightwiki.com/PageWithNumberedLists">Page With Numbered Lists</A></P>\n',
            '<P CLASS="item"><A HREF="http://greenlightwiki.com/PageWithTenVersions">Page With Ten Versions</A></P>\n',
            '<P CLASS="item"><A HREF="http://greenlightwiki.com/PageWithTwoAuthors">Page With Two Authors</A></P>\n',
            '<P CLASS="item"><A HREF="http://greenlightwiki.com/PageWithTwoVersions">Page With Two Versions</A></P>\n',
            '<P CLASS="item"><A HREF="http://greenlightwiki.com/WelcomePage">Welcome Page</A></P>\n',
        ]

        TEST_EQ(expect, [str(para) for para in page.contentParas()])

        page.makeTitle()
        TEST_EQ("All Pages", page.getTitle())

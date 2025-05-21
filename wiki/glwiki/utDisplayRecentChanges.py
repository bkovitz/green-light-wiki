from teest import *
from utMisc import FakeEnvironment

from DisplayRecentChanges import DisplayRecentChanges

import RecentChanges
from WikiRepository import WikiRepository
from Html import OneRowTable, ButtonLink


class ut_DisplayRecentChanges:

    def testContentParas(self):
        page = DisplayRecentChanges(
            FakeEnvironment(WikiRepository("TESTWIKI"), "PageTitle", "George Gibbons")
        )

        expect = RecentChanges.renderHtml("TESTWIKI")

        TEST_EQ(str(expect), str(page.contentParas()))

        TEST_EQ("Recent Changes", page.getTitle())

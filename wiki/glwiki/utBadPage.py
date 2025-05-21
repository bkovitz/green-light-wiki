from teest import *

from BadPage import BadPage

from Chunks import Error404Chunk


class ut_BadPage:

    def testHtmlBody(self):
        page = BadPage("http://test.tld/testpage")

        got = page.htmlBody()

        TEST_EQ(Error404Chunk, got.__class__)
        TEST_EQ("http://test.tld/testpage", got.url)

    def testAll(self):
        page = BadPage("http://test.tld/testpage")

        got = page.renderCgi()

        TEST(got.find(str(page.htmlBody())) >= 0)
        TEST(got.find("Status: 404\n") >= 0)

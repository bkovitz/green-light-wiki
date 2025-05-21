from teest import *
import sys

from CgiEnvironment import CgiEnvironment


class ut_CgiEnvironment:
    """Retrieves from environment dictionary with a few conveniences."""

    def testSimpleGet(self):
        dict = {
            "QUERY_STRING": "PageName",
            "REQUEST_METHOD": "POST",
            "WIKI_DIR": "dir",
        }

        env = CgiEnvironment(dict)

        TEST_EQ(env.get("QUERY_STRING"), "PageName")
        TEST_EQ(env.get("REQUEST_METHOD"), "POST")
        TEST_EQ(env.get("WIKI_DIR"), "dir")
        TEST_EQ(env.get("UNDEFINED_VARIABLE"), "")

    def testQueryStringUnescaped(self):
        dict = {
            "QUERY_STRING": "",
            "QUERY_STRING_UNESCAPED": "PageName",
        }

        env = CgiEnvironment(dict)

        TEST_EQ(env.get("QUERY_STRING"), "PageName")

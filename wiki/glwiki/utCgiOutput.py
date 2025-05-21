from teest import *
import os

from CgiOutput import CgiOutput


class ut_CgiOutput:

    def testCgiOutput(self):
        cgi = CgiOutput("<HTML></HTML>\n")

        expect = """Content-type: text/html

<HTML></HTML>
"""
        TEST_EQ(expect, str(cgi))

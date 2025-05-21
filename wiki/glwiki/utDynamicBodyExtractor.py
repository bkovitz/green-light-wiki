from teest import *
from io import StringIO

from DynamicBodyExtractor import DynamicBodyExtractor


class ut_DynamicBodyExtractor:

    def __init__(self):
        self._input = """<HTML><BODY>
<P>Here is a paragraph.</P>
<P>Here is some text with a {{runme}} inside it</P>
</BODY>
</HTML>
"""

    def testSuccessfulExtraction(self):
        expect = """
<P>Here is a paragraph.</P>
<P>Here is some text with a SAMPLE inside it</P>
"""
        extractor = DynamicBodyExtractor(StringIO(self._input), globals())

        TEST_EQ(expect, extractor.body())

    def testNoScope(self):
        expect = """
<P>Here is a paragraph.</P>
<P>Here is some text with a {{ no WikiCustomizations }} inside it</P>
"""
        extractor = DynamicBodyExtractor(StringIO(self._input), None)

        TEST_EQ(expect, extractor.body())


def runme():
    return "SAMPLE"

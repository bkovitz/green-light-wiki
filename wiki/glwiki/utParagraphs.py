from teest import *

from Paragraphs import Paragraph
from Chunks import ParagraphChunk


class ut_Paragraphs:

    def testRenderHtml(self):
        fakePage = "RequestedPage"

        para = Paragraph(ParagraphChunk, "some text")

        chunk = para.makeChunk(fakePage)
        TEST_EQ(ParagraphChunk, chunk.__class__)
        TEST_EQ("some text", chunk.text)
        TEST_EQ("RequestedPage", chunk.page)

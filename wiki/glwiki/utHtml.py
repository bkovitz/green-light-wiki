from teest import *
import os

from Html import (
    Html,
    HtmlBody,
    HtmlTable,
    HtmlRow,
    HtmlDatum,
    HtmlForm,
    HtmlInputSubmit,
    HtmlInputHidden,
    Standalone,
    Container,
    HtmlHead,
    HtmlTitle,
    HtmlMeta,
    HtmlQuotedAttribute,
    HtmlAnchor,
    HtmlImage,
    HorizontalSpread,
    HtmlAttribute,
    ButtonLink,
    OneRowTable,
    HtmlHolder,
    HtmlPara,
    HardCoded,
    HtmlDiv,
)


class ut_Html:

    def testStandalone(self):
        standalone = Standalone("TAG", 'ATTR="value"')

        expect = '<TAG ATTR="value">'
        TEST_EQ(expect, str(standalone))

    def testContainer(self):
        container = Container("TAG", "some text")

        expect = "<TAG>some text</TAG>\n"
        TEST_EQ(expect, str(container))

        container.add("\nmore text")

        expect = "<TAG>some text\nmore text</TAG>\n"
        TEST_EQ(expect, str(container))

    def testAddPara(self):
        container = Container("TAG")
        container.addPara("some para text")

        expect = "<TAG><P>some para text</P>\n</TAG>\n"
        TEST_EQ(expect, str(container))

    def testAddParaWithClass(self):
        container = Container("TAG")
        container.addPara("some para text", "special")

        expect = '<TAG><P CLASS="special">some para text</P>\n</TAG>\n'
        TEST_EQ(expect, str(container))

    def testHtml(self):
        html = Html("page title")

        expect = """<HTML><HEAD>
  <TITLE>page title</TITLE>
</HEAD>
<BODY></BODY>
</HTML>
"""
        TEST_EQ(expect, str(html))

        expect = Container("HTML")
        head = HtmlHead()
        head.add(HtmlTitle("page title"))
        expect.add(head)
        expect.add(HtmlBody(contents=None))

        TEST_EQ(str(expect), str(html))

    def testHtmlBody(self):
        htmlGenerator = HtmlBody(
            bgcolor=HtmlAttribute("BGCOLOR", "#CCCCCC"), contents="contents"
        )

        expect = "<BODY BGCOLOR=#CCCCCC>contents</BODY>\n"
        TEST_EQ(expect, str(htmlGenerator))

    def testHtmlAnchor(self):
        htmlGenerator = HtmlAnchor("url", "text")

        expect = '<A HREF="url">text</A>'
        TEST_EQ(expect, str(htmlGenerator))

    def testHtmlAnchorInsideIndentedContainer(self):
        htmlGenerator = HtmlDatum(HtmlAnchor("url", "text"))

        expect = """<TD>
  <A HREF="url">text</A>
</TD>
"""
        TEST_EQ(expect, str(htmlGenerator))

    def testStandaloneInsideIndentedContainer(self):
        htmlGenerator = HtmlDatum([HtmlAnchor("url1", HtmlImage("url2"))])

        expect = """<TD>
  <A HREF="url1"><IMG SRC="url2" BORDER=0></A>
</TD>
"""
        TEST_EQ(expect, str(htmlGenerator))

    def testNone(self):
        htmlGenerator = Html()
        htmlGenerator.add(None)
        expect = Html("")

        TEST_EQ(str(expect), str(htmlGenerator))

    def testRenderingAList(self):
        htmlGenerator = Html([HtmlAnchor("test", "test")])

        expect = Html(HtmlAnchor("test", "test"))

        TEST_EQ(str(expect), str(htmlGenerator))

    def testHtmlTable(self):
        htmlTable = HtmlTable(
            [
                HtmlRow(
                    [
                        HtmlDatum("cell 1"),
                        HtmlDatum("cell 2"),
                    ]
                ),
                HtmlRow(
                    [
                        HtmlDatum("cell 3"),
                        HtmlDatum("cell 4"),
                        HtmlDatum("cell 5"),
                    ]
                ),
            ]
        )

        expect = """<TABLE>
  <TR>
    <TD>
      cell 1
    </TD>
    <TD>
      cell 2
    </TD>
  </TR>
  <TR>
    <TD>
      cell 3
    </TD>
    <TD>
      cell 4
    </TD>
    <TD>
      cell 5
    </TD>
  </TR>
</TABLE>
"""
        TEST_EQ(expect, str(htmlTable))

    def testHtmlForm(self):
        htmlForm = HtmlForm(action="action", method="GET", items="input")

        expect = '<FORM ACTION="action" METHOD=GET>input</FORM>'

        TEST_EQ(expect, str(htmlForm))

    def testHtmlInputSubmit(self):
        htmlInput = HtmlInputSubmit("buttonText")

        expect = '<INPUT TYPE=SUBMIT VALUE="buttonText">'
        TEST_EQ(expect, str(htmlInput))

    def testHtmlInputHidden(self):
        htmlInput = HtmlInputHidden("name", "value")

        expect = '<INPUT TYPE=HIDDEN NAME="name" VALUE="value">'
        TEST_EQ(expect, str(htmlInput))

    def testEscapeQuotes(self):
        expect = 'ATTR="value with &#34;quoted text&#34;"'
        got = HtmlQuotedAttribute("ATTR", 'value with "quoted text"')

        TEST_EQ(expect, str(got))

    def testHorizontalSpread(self):
        expect = HtmlTable(
            attrs=HtmlAttribute("WIDTH", "100%"),
            data=[
                HtmlRow(
                    [
                        HtmlDatum("left item", HtmlAttribute("ALIGN", "LEFT")),
                        HtmlDatum("right item", HtmlAttribute("ALIGN", "RIGHT")),
                    ]
                )
            ],
        )

        got = HorizontalSpread(
            left="left item",
            right="right item",
        )

        TEST_EQ(str(expect), str(got))

    def testButtonLink(self):
        expect = HtmlForm(
            action="action", method="GET", items=HtmlInputSubmit(" Button ")
        )

        got = ButtonLink("action", " Button ")

        TEST_EQ(str(expect), str(got))

    def testOneRowTable(self):
        expect = HtmlTable(
            [
                HtmlRow(
                    [
                        HtmlDatum("cell 1"),
                        HtmlDatum("cell 2"),
                        HtmlDatum("cell 3"),
                    ],
                    HtmlQuotedAttribute("VALIGN", "BASELINE"),
                )
            ]
        )

        got = OneRowTable(["cell 1", "cell 2", "cell 3"])

        TEST_EQ(str(expect), str(got))

    def testHtmlHolder(self):
        expect = "<BR>" + str(HtmlAnchor("url", "text"))

        got = HtmlHolder(["<BR>", HtmlAnchor("url", "text")])

        TEST_EQ(expect, str(got))

    def testParaTrimsClosingNewline(self):
        expect = "<P>a paragraph</P>\n"

        got = HtmlPara("a paragraph\n")

        TEST_EQ(expect, str(got))

    def testHardCoded(self):
        class SomeHtml(HardCoded):

            def rawHtml(self):
                return "<P>Some raw Html.</P>"

        got = SomeHtml()
        expect = "<P>Some raw Html.</P>"

        TEST_EQ(expect, str(got))

    def testHardCodedWithIndent(self):
        class SomeHtml(HardCoded):

            def rawHtml(self):
                return "<P>Some raw Html.</P>"

        got = HtmlDiv(data=SomeHtml())
        expect = """<DIV>
  <P>Some raw Html.</P>
</DIV>
"""

        TEST_EQ(expect, str(got))

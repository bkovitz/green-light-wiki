# from types import ListType, StringType, IntType

from Indent import Indent
from Misc import makeList


class Standalone:

    def __init__(self, tag, attrs=None, newlineAfter=0):
        self.tag = tag

        # TODO: call _makeList
        if isinstance(attrs, list):
            self.attrs = attrs
        elif attrs == None:
            self.attrs = []
        else:
            self.attrs = [attrs]

        self.newlineAfter = newlineAfter

    def __str__(self):
        return self.render(Indent())

    def __repr__(self):
        return "<%s instance: '%s'>" % (self.__class__.__name__, str(self))

    def render(self, indent, isBeginningOfLine=1):
        attrs, items = self._preprocess()
        return (
            indent.render(isBeginningOfLine)
            + self._renderOpeningTag(attrs)
            + self._termination()
        )

    def _preprocess(self):
        """override in derived classes"""
        return self.attrs, None

    def _renderOpeningTag(self, attrs):
        result = "<" + self.tag
        if attrs != None:
            for attr in attrs:
                if attr:
                    result += " " + str(attr)
        result += ">"

        return result

    def _termination(self):
        if self.newlineAfter:
            return "\n"
        else:
            return ""

    def __getattr__(self, name):
        if name == "newlineAfter":
            return 0
        else:
            raise AttributeError(name)


class Container(Standalone):

    def __init__(self, tag, items=None, attrs=None, indentsChildren=0, newlineAfter=1):
        self.tag = tag

        self.items = makeList(items)
        self.attrs = makeList(attrs)

        self.indentsChildren = indentsChildren
        self.newlineAfter = newlineAfter

    def add(self, item):
        if isinstance(item, list):
            self.items += item
        else:
            self.items.append(item)

    def addPara(self, paraText, class_=None):
        if class_:
            p = HtmlPara(paraText, HtmlQuotedAttribute("CLASS", class_))
        else:
            p = HtmlPara(paraText)
        self.items.append(p)

    def render(self, indent, isBeginningOfLine=0):
        attrs, items = self._preprocess()

        result = indent.render(isBeginningOfLine) + self._renderOpeningTag(attrs)

        if self.indentsChildren:
            indent.increment()
            result += "\n"

        result += self._renderItems(indent, items)

        if self.indentsChildren:
            indent.decrement()
            if result[-1] != "\n":
                result += "\n"

        result += self._renderClosingTag(indent) + self._termination()

        return result

    def getItems(self):
        return self.items

    def _preprocess(self):
        """override in derived classes"""
        return self.attrs, self.items

    def _renderItems(self, indent, items):
        result = ""
        isFirstOnLine = 1
        for item in items:
            result += self._renderItem(
                item, indent, isFirstOnLine and self.indentsChildren
            )

            if len(result) > 0:
                isFirstOnLine = result[-1] == "\n"

        return result

    def _renderClosingTag(self, indent):
        return "%s</%s>" % (indent.render(self.indentsChildren), self.tag)

    def _renderItem(self, item, indent, isFirstOnLine):
        result = ""

        # if type(item) == StringType or type(item) == IntType:
        if isinstance(item, (str, int)):
            if self.indentsChildren:
                result += indent.render(isFirstOnLine)
            result += str(item)
        # elif type(item) == ListType:
        elif isinstance(item, list):
            result += self._renderItems(indent, item)
        elif item:
            result += item.render(indent, isFirstOnLine)

        return result

    # TODO: delete
    def _makeList(self, obj):
        # if type(obj) == ListType:
        if isinstance(obj, list):
            return obj
        else:
            return [obj]


class HtmlAttribute:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return "%s=%s" % (self.name, self.value)


class HtmlQuotedAttribute:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return '%s="%s"' % (self.name, _escapeQuotes(self.value))


class Html(Container):

    def __init__(
        self,
        title=None,
        # bgcolor=HtmlAttribute("BGCOLOR", "#FFFFFF")
        bgcolor=None,
    ):
        self.bgcolor = bgcolor
        Container.__init__(self, "HTML")
        self.head = HtmlHead()
        if title:
            self.head.add(HtmlTitle(title))

    def _preprocess(self):
        return self.attrs, [self.head, HtmlBody(self.items, self.bgcolor)]

    def addHeadItem(self, item):
        self.head.add(item)


class HtmlHead(Container):

    def __init__(self):
        Container.__init__(self, "HEAD", indentsChildren=1)


def _escapeQuotes(s):
    return s.replace('"', "&#34;")


class HtmlPara(Container):

    def __init__(self, data=None, attrs=None):
        Container.__init__(self, "P", data, attrs, newlineAfter=1)

    def _preprocess(self):
        # if type(self.items[-1]) == StringType:
        if isinstance(self.items[-1], str):
            self.items[-1] = self.items[-1].rstrip()

        return (self.attrs, self.items)


class Span(Container):

    def __init__(self, class_=None, data=None):
        Container.__init__(
            self, "SPAN", data, attrIfNotNone("CLASS", class_), newlineAfter=0
        )


class HtmlAnchor(Container):

    def __init__(self, href=None, data=None, attrs=None):
        self.href = href
        Container.__init__(self, "A", data, attrs, newlineAfter=0)

    def _preprocess(self):
        return ([HtmlQuotedAttribute("HREF", self.href)] + self.attrs, self.items)


class H1(Container):

    def __init__(self, data=None, attrs=None):
        Container.__init__(self, "H1", data, attrs, newlineAfter=1)


class H2(Container):

    def __init__(self, data=None, attrs=None):
        Container.__init__(self, "H2", data, attrs, newlineAfter=1)


class Hn(Container):

    def __init__(self, headingLevel, data=None, attrs=None):
        Container.__init__(self, "H%d" % int(headingLevel), data, attrs, newlineAfter=1)


class Class(HtmlQuotedAttribute):

    def __init__(self, class_):
        HtmlQuotedAttribute.__init__(self, "CLASS", class_)


class Id(HtmlQuotedAttribute):

    def __init__(self, id):
        HtmlQuotedAttribute.__init__(self, "ID", id)


class HtmlImage(Standalone):

    def __init__(self, src):
        Standalone.__init__(
            self, "IMG", [HtmlQuotedAttribute("SRC", src), HtmlAttribute("BORDER", 0)]
        )


class HtmlTitle(Container):

    def __init__(self, title):
        Container.__init__(self, "TITLE", [title])


class HtmlBody(Container):

    def __init__(self, contents, bgcolor=None):
        Container.__init__(self, "BODY", contents, bgcolor, newlineAfter=1)


class HtmlDiv(Container):

    def __init__(self, class_=None, id=None, data=None):
        Container.__init__(
            self,
            tag="DIV",
            items=data,
            attrs=classAndIdAttrs(class_, id),
            indentsChildren=1,
            newlineAfter=1,
        )


def classAndIdAttrs(class_, id):
    result = []
    classAttr = attrIfNotNone("CLASS", class_)
    if classAttr:
        result.append(classAttr)
    idAttr = attrIfNotNone("ID", id)
    if idAttr:
        result.append(idAttr)

    if not result:
        return None
    elif len(result) == 1:
        return result[0]
    else:
        return result


def attrIfNotNone(tag, value):
    if value:
        return HtmlQuotedAttribute(tag, str(value))
    else:
        return None


class HtmlTable(Container):

    def __init__(self, data=None, attrs=None):
        Container.__init__(
            self, "TABLE", data, attrs, indentsChildren=1, newlineAfter=1
        )


class HtmlRow(Container):

    def __init__(self, data=None, attrs=None):
        Container.__init__(self, "TR", data, attrs, indentsChildren=1)


class HtmlDatum(Container):

    def __init__(self, data=None, attrs=None):
        Container.__init__(self, "TD", data, attrs, indentsChildren=1)


class HtmlForm(Container):

    def __init__(self, action, method, items, normalFormatting=0):
        Container.__init__(
            self,
            "FORM",
            items,
            [
                HtmlQuotedAttribute("ACTION", action),
                HtmlAttribute("METHOD", method),
            ],
            indentsChildren=normalFormatting,
            newlineAfter=normalFormatting,
        )


class HtmlInputSubmit(Standalone):

    def __init__(self, button, attrs=None):
        Standalone.__init__(
            self,
            "INPUT",
            [
                HtmlAttribute("TYPE", "SUBMIT"),
                HtmlQuotedAttribute("VALUE", button),
                attrs,
            ],
        )


class HtmlInputHidden(Standalone):

    def __init__(self, name, value):
        Standalone.__init__(
            self,
            "INPUT",
            [
                HtmlAttribute("TYPE", "HIDDEN"),
                HtmlQuotedAttribute("NAME", str(name)),
                HtmlQuotedAttribute("VALUE", str(value)),
            ],
        )


class HtmlInputText(Standalone):

    def __init__(self, name, value=None, size=None, maxLength=None):
        Standalone.__init__(
            self,
            "INPUT",
            [
                HtmlAttribute("TYPE", "TEXT"),
                HtmlQuotedAttribute("NAME", str(name)),
                attrIfNotNone("VALUE", value),
                attrIfNotNone("SIZE", size),
                attrIfNotNone("MAXLENGTH", maxLength),
            ],
        )


class HtmlMeta(Standalone):

    def __init__(self, name, content):
        Standalone.__init__(
            self,
            "META",
            [
                HtmlQuotedAttribute("NAME", name),
                HtmlQuotedAttribute("CONTENT", content),
            ],
            newlineAfter=1,
        )


class NoRobots(HtmlMeta):

    def __init__(self):
        HtmlMeta.__init__(self, "robots", "none")


class HtmlLink(Standalone):

    def __init__(self, rel, href, type):
        Standalone.__init__(
            self,
            "LINK",
            [
                HtmlQuotedAttribute("REL", rel),
                HtmlQuotedAttribute("HREF", href),
                HtmlQuotedAttribute("TYPE", type),
            ],
            newlineAfter=1,
        )


class HtmlRefresh(Standalone):

    def __init__(self, seconds, url):
        Standalone.__init__(
            self,
            "META",
            [
                HtmlQuotedAttribute("HTTP-EQUIV", "refresh"),
                HtmlQuotedAttribute("CONTENT", "%d; %s" % (seconds, url)),
            ],
            newlineAfter=1,
        )


class HtmlTextArea(Container):

    def __init__(self, name, text):
        Container.__init__(
            self,
            "TEXTAREA",
            text,
            [
                HtmlAttribute("ROWS", 24),
                HtmlAttribute("COLS", 80),
                HtmlAttribute("WRAP", "VIRTUAL"),
                HtmlQuotedAttribute("NAME", name),
            ],
        )


class HtmlUnorderedList(Container):

    def __init__(self, data=None, attrs=None):
        Container.__init__(self, "UL", data, attrs, indentsChildren=1, newlineAfter=1)


class HtmlOrderedList(Container):

    def __init__(self, data=None, attrs=None):
        Container.__init__(self, "OL", data, attrs, indentsChildren=1, newlineAfter=1)


class HtmlListItem(Container):

    def __init__(self, data=None, attrs=None):
        Container.__init__(self, "LI", data, attrs, indentsChildren=0, newlineAfter=1)


# TODO: probably better to inherit from HtmlTable
class HorizontalSpread(Container):

    def __init__(self, left, right, attrs=None):
        Container.__init__(
            self,
            tag="TABLE",
            items=left,
            attrs=attrs,
            indentsChildren=1,
            newlineAfter=1,
        )
        self.right = right

    def _preprocess(self):
        return [HtmlAttribute("WIDTH", "100%")] + self.attrs, [
            HtmlRow(
                [
                    HtmlDatum(self.items, HtmlAttribute("ALIGN", "LEFT")),
                    HtmlDatum(self.right, HtmlAttribute("ALIGN", "RIGHT")),
                ]
            )
        ]


class ButtonLink(HtmlForm):

    def __init__(self, url, buttonText):
        HtmlForm.__init__(self, url, "GET", HtmlInputSubmit(buttonText))


class OneRowTable(HtmlTable):

    def __init__(self, data=None, attrs=None):
        HtmlTable.__init__(
            self,
            data,
        )

    def _preprocess(self):
        return (
            self.attrs,
            [
                HtmlRow(
                    [HtmlDatum(item) for item in self.items],
                    makeList(self.attrs) + [HtmlQuotedAttribute("VALIGN", "BASELINE")],
                )
            ],
        )


class ListRow(HtmlTable):

    def __init__(self, leftColumn, rightColumn):
        self.leftColumn = leftColumn
        self.rightColumn = rightColumn
        self.leftWidth = [
            HtmlAttribute("WIDTH", "20"),
            HtmlAttribute("VALIGN", "BASELINE"),
        ]
        HtmlTable.__init__(self, None, None)

    def _preprocess(self):
        return self.attrs, [
            HtmlRow(
                [
                    HtmlDatum(self.leftColumn, self.leftWidth),
                    HtmlDatum(self.rightColumn),
                ]
            )
        ]


class HtmlHolder(Container):

    def __init__(self, items=None):
        self.items = makeList(items)
        self.indentsChildren = 0

    def add(self, item):
        self.items.append(item)

    def __str__(self):
        return self.render(Indent())

    def render(self, indent, isBeginningOfLine=0):
        return self._renderItems(indent, self.items)


class HardCoded(Standalone):

    def __init__(self):
        pass

    def rawHtml(self):
        raise "abstract class: need override"

    def render(self, indent, isBeginningOfLine=1):
        return indent.render(isBeginningOfLine) + self.rawHtml()

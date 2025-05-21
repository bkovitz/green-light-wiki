from Html import HtmlTable, HtmlRow, HtmlDatum, HtmlQuotedAttribute


class ClassedDatum(HtmlDatum):

    def __init__(self, className):
        HtmlDatum.__init__(self, attrs=HtmlQuotedAttribute("CLASS", className))
        self.indentsChildren = 0


class StoryRectangle(HtmlTable):

    def __init__(self, contents):
        HtmlTable.__init__(
            self,
            contents,
            [
                HtmlQuotedAttribute("CLASS", "story"),
                HtmlQuotedAttribute("CELLPADDING", "0"),
                HtmlQuotedAttribute("CELLSPACING", "0"),
            ],
        )

    def _preprocess(self):
        return (
            self.attrs,
            [
                HtmlRow(
                    [
                        ClassedDatum("story-tl"),
                        ClassedDatum("story-t"),
                        ClassedDatum("story-tr"),
                    ]
                ),
                HtmlRow(
                    [
                        ClassedDatum("story-l"),
                        HtmlDatum(self.items),
                        ClassedDatum("story-r"),
                    ]
                ),
                HtmlRow(
                    [
                        ClassedDatum("story-bl"),
                        ClassedDatum("story-b"),
                        ClassedDatum("story-br"),
                    ]
                ),
            ],
        )

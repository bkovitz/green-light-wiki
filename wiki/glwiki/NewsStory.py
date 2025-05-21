from Date import Date
from StoryRectangle import StoryRectangle
from Html import H1, HtmlPara, Span, HtmlHolder
from WikiText2 import WikiText2


def isBlank(s):
    return len(s) == 0


class StoryParser:

    def __init__(self, newsStory):
        self._newsStory = newsStory
        self._state = self._expectTitle

    def feedLine(self, line):
        self._state(line.strip())

    # parser states

    def _expectTitle(self, line):
        if not isBlank(line):
            self._newsStory.setTitle(line)
            self._state = self._expectDate

    def _expectDate(self, line):
        if not isBlank(line):
            self._newsStory.setDate(line)
            self._state = self._expectBody

    def _expectBody(self, line):
        if not isBlank(line):
            self._newsStory.setBody(line)
            self._state = self._inBody

    def _inBody(self, line):
        self._newsStory.appendBody(line)


class NewsStory:

    def __init__(self, file_):
        self._title = ""
        self._date = ""
        self._body = []

        parser = StoryParser(self)

        for line in file_:
            parser.feedLine(line)

        file_.close()

    def getTitle(self):
        return self._title

    def getDate(self):
        return self._date

    def getBody(self):
        return self._body

    def setTitle(self, title):
        self._title = title

    def setDate(self, date):
        self._date = Date(date)

    def setBody(self, line):
        self._body = [line]

    def appendBody(self, line):
        self._body.append(line)

    def getSummary(self):
        result = []
        for line in self._body:
            if isBlank(line):
                if not isBlank(result):
                    break
            else:
                result.append(line)

        return result

    def getSummaryRectangle(self):
        wikiSummary = WikiText2(
            [HtmlHolder([self._makeDate(), " "])] + self.getSummary()
        )
        wikiHtml = wikiSummary.renderHtml()

        return StoryRectangle(
            [H1(self.getTitle()), "".join([str(para) for para in wikiHtml])]
        )

    def _makeDate(self):
        return Span("date", "(" + str(self.getDate()) + ")")

import re, operator
from functools import reduce

from DictWithGetAttr import DictWithGetAttr

_tokenTypes = re.compile(r"((?:<%=)|(?:%>)|(?:\\.))")

ST_START = 0
ST_IN_EXPRESSION = 1

ST_START_CHUNK = 2
ST_IN_CHUNK = 3


class HtmlChunk:

    def __init__(self, templateString):
        self._tokens = _tokenTypes.split(_makeString(templateString))

    def __str__(self):
        result = ""
        expression = ""
        state = ST_START
        self._dict = DictWithGetAttr(self)

        for token in self._tokens:
            if not token:
                continue
            if state == ST_START:
                if token == "<%=":
                    state = ST_IN_EXPRESSION
                    expression = ""
                elif token[0] == "\\":
                    result += _deBackslash(token)
                else:
                    result += token
            else:
                assert state == ST_IN_EXPRESSION
                if token == "%>":
                    state = ST_START
                    result += _makeString(self._evalWithSpecialDict(expression))
                elif token[0] == "\\":
                    expression += _deBackslash(token)
                else:
                    expression += token

        return result

    def __eq__(self, other):
        return self.__class__ == other.__class__ and reduce(
            operator.__and__,
            map(
                lambda a, b: str(a) == str(b),
                self._listOfVarsAndValues(),
                other._listOfVarsAndValues(),
            ),
        )

    def __ne__(self, other):
        return not self == other

    def _listOfVarsAndValues(self):
        result = []
        for var in self._listOfVars():
            try:
                result.append([var, self.__dict__[var]])
            except KeyError:
                pass

        return result

    def _listOfVars(self):
        return [var for var in dir(self) if not var.startswith("_") and var != "page"]

    def __repr__(self):
        return "<%s instance: '%s'>" % (self.__class__.__name__, str(self).rstrip())

    def __hash__(self):
        return hash(str(self))

    def render(self, ignored, ignored2):
        return str(self)

    def _evalWithSpecialDict(self, expression):
        """Thank you, http://groups.google.com/groups?th=a319a98144d6def7"""
        compiled = compile(expression.strip(), "<string>", "eval")
        realDict = {}
        for varName in compiled.co_names:
            realDict[varName] = self._dict[varName]
        return eval(compiled, globals(), realDict)


class HtmlChunkFromFile(HtmlChunk):

    def __init__(self, file_, chunkName, default=""):
        self.setChunk(file_, chunkName, default)

    def setChunk(self, file_, chunkName, default=""):
        self._tokens = _tokenTypes.split(_extractChunk(file_, chunkName, default))


def _extractChunk(file_, chunkName, default):
    chunk = ""
    possiblePartOfChunk = ""

    chunkLeader = re.compile(r"==\s*" + re.escape(chunkName) + "\s*\n$")
    chunkEnd = re.compile("==\s*[^=]*\s*\n$")

    state = ST_START

    file_.seek(0)
    for line in file_:
        if state == ST_START:
            if chunkLeader.match(line):
                state = ST_START_CHUNK
        elif state == ST_START_CHUNK:
            if line.strip():
                chunk = line
                state = ST_IN_CHUNK
        else:
            assert state == ST_IN_CHUNK
            if chunkEnd.match(line):
                break
            if line.strip():
                if possiblePartOfChunk:
                    chunk += possiblePartOfChunk
                    possiblePartOfChunk = ""
                chunk += line
            else:
                possiblePartOfChunk += line

    if state == ST_START:
        return default
    else:
        return chunk


_backslashCodes = {
    "n": "\n",
    "r": "\r",
    "f": "\f",
}


def _deBackslash(twoCharString):
    assert twoCharString[0] == "\\"
    letter = twoCharString[1]
    if letter in _backslashCodes:
        return _backslashCodes[letter]
    else:
        return letter


def _makeString(s):
    if s is None:
        s = ""
    elif isinstance(s, list) or isinstance(s, tuple):
        s = "".join([str(item) for item in s])

    return str(s)

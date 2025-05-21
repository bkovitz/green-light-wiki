from TextFile import TextFile


class HashFile:

    def __init__(self, filename):
        self._parser = CommaSeparatedLineParser()
        self._dict = {}
        self._dirty = False
        self._textfile = TextFile(filename)
        self._readDict()

    def __del__(self):
        if self._dirty:
            self._textfile.write(
                [
                    self._commaSeparated(key, value)
                    # for key, value in self._dict.iteritems()
                    for key, value in self._dict.items()
                ]
            )

    def __setitem__(self, key, value):
        self._dict[key] = value
        self._dirty = True

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def _commaSeparated(self, key, value):
        return self._quote(key) + "," + self._quote(value)

    def _quote(self, s):
        s = str(s)
        if "\n" in s or "," in s or '"' in s or " " in s:
            return '"' + self._backslash(s) + '"'
        else:
            return s

    def _backslash(self, s):
        result = ""
        for c in s:
            if c == '"':
                result += '"'
            elif c == "\n":
                result += "\\n"
            else:
                result += c

        return result

    def _readDict(self):
        self._dict = {}
        for line in self._textfile:
            # key, value = self._parser.parseLine(line)
            got = self._parser.parseLine(line)
            # print("GOT", got)
            key, value = got
            self._dict[key] = value


# parser states
ST_START = 0
ST_IN_QUOTED = 1
ST_GOT_BACKSLASH = 2
ST_BETWEEN_ITEMS = 3


class CommaSeparatedLineParser:

    def parseLine(self, line):
        self.result = []
        self.currentIndex = 0
        state = ST_START
        for c in line:
            if state == ST_START:
                if c == '"':
                    state = ST_IN_QUOTED
                elif c == ",":
                    self.currentIndex += 1
                else:
                    self._appendChar(c)
            elif state == ST_IN_QUOTED:
                if c == '"':
                    state = ST_BETWEEN_ITEMS
                elif c == "\\":
                    state = ST_GOT_BACKSLASH
                else:
                    self._appendChar(c)
            elif state == ST_GOT_BACKSLASH:
                if c == "n":
                    self._appendChar("\n")
                else:
                    self._appendChar(c)
                state = ST_IN_QUOTED
            else:
                assert state == ST_BETWEEN_ITEMS
                if c == ",":
                    state = ST_START
                    self.currentIndex += 1

        return self.result

    def _appendChar(self, c):
        if self.currentIndex >= len(self.result):
            self.result.append("")
        self.result[self.currentIndex] += c

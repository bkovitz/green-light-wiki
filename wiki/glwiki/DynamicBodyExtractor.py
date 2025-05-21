import re

from BodyExtractor import BodyExtractor

braceFinder = re.compile("({{)|(}})")


class DynamicBodyExtractor(BodyExtractor):

    def __init__(self, inputFile, scopeDict):
        BodyExtractor.__init__(self, inputFile)
        self._scopeDict = scopeDict

    def mungeData(self, data):
        result = ""

        betweenBraces = 0
        subroutine = ""

        for chunk in re.split(braceFinder, data):
            if not chunk:
                continue

            if not betweenBraces and chunk == "{{":
                betweenBraces = 1
                subroutine = ""
            elif betweenBraces and chunk == "}}":
                try:
                    result += self._scopeDict[subroutine]()
                except TypeError:
                    result += "{{ no WikiCustomizations }}"
                except KeyError:
                    result += (
                        "{{ %s does not exist in WikiCustomizations }}" % subroutine
                    )
                betweenBraces = 0
            elif betweenBraces:
                subroutine = chunk
            else:
                result += chunk

        return result

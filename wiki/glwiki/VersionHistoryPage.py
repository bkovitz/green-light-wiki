from DisplayPage import DisplayPage

from Chunks import VersionHistoryItemChunk, VersionHistoryChunk


class VersionHistoryPage(DisplayPage):

    def getCommand(self):
        return "VER"

    def getContent(self):
        return VersionHistoryChunk(
            self,
            [
                self._makeVersionHistoryItemChunk(versionNum)
                for versionNum in range(
                    1, self.getVersionManager().getLatestVersionNum() + 1
                )
            ],
        )

    def _makeVersionHistoryItemChunk(self, versionNum):
        version = self.getVersionManager().getVersionInfo(versionNum)
        plus, minus = self.getVersionManager().getPlusMinus(versionNum)

        return VersionHistoryItemChunk(
            self,
            versionNum,
            version.date,
            version.author,
            makePlusMinusString(plus, minus),
        )


def makePlusMinusString(plus, minus):
    result = ""

    if plus:
        result += "+" + str(plus)

    if minus:
        if result:
            result += " "
        result += "-" + str(minus)

    return result

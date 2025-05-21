from MightRequireLogin import MightRequireLogin
from Html import (
    Html,
    HtmlMeta,
    HtmlForm,
    HtmlTextArea,
    HtmlInputSubmit,
    HtmlInputHidden,
    HtmlDiv,
    HtmlPara,
    HtmlAnchor,
    NoRobots,
)
from Config import config
from UnsmashWords import unsmashWords
from VersionedFile2 import VersionedFile2
from Chunks import EditContentChunk


class EditPage(MightRequireLogin):

    def getCommand(self):
        return "EDIT"

    def getTitle(self):
        return "edit " + unsmashWords(self.getPageName())

    def contentDiv(self):
        if self.needLogin():
            return self.loginDiv()
        else:
            return self.editDiv()

    def headItems(self):
        return NoRobots()

    def loginDiv(self):
        return self.genericLoginDiv(
            "edit",
            HtmlPara(
                [
                    "You need to log in before you can edit ",
                    HtmlAnchor(  # TODO: add the appropriate CLASS
                        config.makeUrl(
                            self.getWikiName(),
                            self.getPageName(),
                        ),
                        unsmashWords(self.getPageName()),
                    ),
                    ".",
                ]
            ),
        )

    def editDiv(self):
        div = HtmlDiv(id="wiki-edit")
        div.add(
            HtmlForm(
                action=config.makeUrl(self._repository.getWikiName(), self._pageName),
                method="POST",
                items=[
                    HtmlTextArea("text", self.text()),
                    HtmlDiv(
                        id="wiki-edit-buttons",
                        data=[
                            HtmlInputSubmit(" Save "),
                            HtmlInputHidden("origVersion", self._maxVersionNum()),
                        ],
                    ),
                ],
            )
        )

        return div

    def logo(self):
        return None

    def buttonsDiv(self):
        return None

    def getContent(self):
        return EditContentChunk(
            self, self.getPageUrl(), self.text(), self._maxVersionNum()
        )

    def makeMetas(self):
        self._metas = NoRobots()

    def getButtons(self):
        return None

    def text(self):
        # TODO: OAOO with Display._readlines()
        f = self._openForReading()
        if f:
            versionManager = VersionedFile2(f)
            result = versionManager.getLatestVersion()
            f.close()
        else:
            result = [""]

        return result

    def _maxVersionNum(self):
        f = self._openForReading()
        if f:
            versionManager = VersionedFile2(f)
            result = versionManager.getLatestVersionNum()
            f.close()
        else:
            result = 0

        return result

    def _openForReading(self):
        return self._repository.pageFile(self.getPageName()).openForReading()

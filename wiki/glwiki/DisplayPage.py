import os
from difflib import SequenceMatcher

from WikiPage import WikiPage
from WikiText2 import WikiText2
from VersionedFile2 import VersionedFile2, VersionInfo, BadVersionException
from Html import (
    Html,
    HtmlTable,
    HtmlRow,
    HtmlDatum,
    HtmlLink,
    HtmlAttribute,
    OneRowTable,
    HtmlForm,
    HtmlInputSubmit,
    HtmlInputHidden,
    ButtonLink,
    HtmlMeta,
    HtmlAnchor,
    HtmlImage,
    HtmlPara,
    Class,
)
from Config import config
from HtmlMisc import metaKeywords
from Chunks import (
    BadVersionNumberChunk,
    LinkToExistingPageChunk,
    VersionInfoChunk,
    ChangedParagraphChunk,
)
from CommandLine import cmdArgs
import SessionDatabase


class NoVersionNumber(Exception):
    pass


class RangeList:

    def __init__(self):
        self._list = []

    def append(self, lowerBound, upperBound):
        """lowerBound is inclusive, upperBound is exclusive, just like other
        Python ranges"""
        self._list.append([lowerBound, upperBound])

    def hasIndexInRange(self, index):
        for range_ in self._list:
            if index >= range_[0] and index < range_[1]:
                return True

        return False


class DisplayPage(WikiPage):

    def __init__(self, environment, actualPageName=None):
        WikiPage.__init__(self, environment)
        if not actualPageName:
            actualPageName = WikiPage.getPageName(self)
        self._actualPageName = actualPageName
        self._versionManager = VersionedFile2(self._openForReading())

    def getPageName(self):
        return self._actualPageName

    def getCommand(self):
        return "DISP"

    def getVersionManager(self):
        return self._versionManager

    def getMessage(self):
        messageChunkClass, args = SessionDatabase.getPendingMessage(self.getSessionId())

        if messageChunkClass is not None:
            return apply(messageChunkClass, (self,) + args + (self.getRepository(),))

    def contentParas(self):
        requestedVersionNumber = self._getRequestedVersionNumber()
        requestedWikiText = self._wikiText(
            self._versionManager.getVersion(requestedVersionNumber)
        )
        previousAuthorsWikiText = self._wikiText(
            self._versionManager.getPreviousAuthorsLastEdit(requestedVersionNumber)
        )

        if previousAuthorsWikiText:
            holders = self._changeBars(previousAuthorsWikiText, requestedWikiText)
        else:
            holders = requestedWikiText

        paragraphs = [holder.makeChunk(self) for holder in holders]

        # put numbers in the numbered lists
        listItemNumber = 0
        for paragraph in paragraphs:
            if paragraph.isListBreak():
                listItemNumber = 0
            if paragraph.needsNumber():
                listItemNumber += 1
                paragraph.number = listItemNumber

        return paragraphs

    def _wikiText(self, version):
        if version is None:
            return None
        else:
            return WikiText2(version, self.getRepository()).makeParas()

    def _changeBars(self, previousAuthorsWikiText, requestedWikiText):
        unchangedRanges = RangeList()
        matcher = SequenceMatcher(None)
        matcher.set_seqs(previousAuthorsWikiText, requestedWikiText)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                unchangedRanges.append(j1, j2)

        wikiTextWithChangeBars = requestedWikiText[:]
        for index in range(len(wikiTextWithChangeBars)):
            if not unchangedRanges.hasIndexInRange(index):
                wikiTextWithChangeBars[index].makeChanged()

        return wikiTextWithChangeBars

    def buttons(self):
        try:
            versionInfo = self._versionManager.getVersionInfo(
                self._getRequestedVersionNumber()
            )
        # except BadVersionException, e:
        except BadVersionException as e:
            versionInfo = VersionInfo(e.versionNum, "(unknown)", "(unknown)")

        return [
            self.editButton(),
            self.historyButton(),
            self.homeButton(),
            self.recentButton(),
            self.allButton(),
            VersionInfoChunk(
                self, versionInfo.versionNum, versionInfo.date, versionInfo.author
            ),
        ]

    def editButton(self):
        return HtmlForm(
            action=config.makeUrl(self.getWikiName(), self.getPageName()),
            method="GET",
            items=[
                HtmlInputSubmit("  Edit  ", attrs=Class("edit")),
                HtmlInputHidden("action", "edit"),
            ],
        )

    def buttonSpacer(self):
        return HtmlDiv(class_="spacer", data="&nbsp;")

    def homeButton(self):
        return ButtonLink(config.homeUrl(self.getWikiName()), " Home ")

    def recentButton(self):
        return ButtonLink(
            config.makeUrl(self.getWikiName(), "RecentChanges"), " Recent "
        )

    def allButton(self):
        return ButtonLink(config.makeUrl(self.getWikiName(), "AllPages"), "  All  ")

    def historyButton(self):
        return HtmlForm(
            action=self.getPageUrl(),
            method="GET",
            items=[HtmlInputSubmit(" History "), HtmlInputHidden("action", "history")],
        )

    def _readlines(self):
        return self._versionManager.getVersion(self._getRequestedVersionNumber())

    def _getPageFile(self):
        return self._repository.pageFile(self.getPageName())

    def _openForReading(self):  # TODO: OAOO
        return self._repository.pageFile(self.getPageName()).openForReading()

    def _getRequestedVersionNumber(self):
        try:
            return int(self.getQueryDict()["version"][0])
        except KeyError:
            return self._versionManager.getLatestVersionNum()

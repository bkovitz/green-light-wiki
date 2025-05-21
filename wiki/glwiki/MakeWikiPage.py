from DisplayPage import DisplayPage
from EditNewPage import EditNewPage
from EditPage import EditPage
from SavePage import SavePage
from DisplayRecentChanges import DisplayRecentChanges
from DisplayAllPages import DisplayAllPages
from VersionHistoryPage import VersionHistoryPage
from Login import Login
from WikiRepository import WikiRepository
from Config import config


def makeWikiPage(environment):
    repository = WikiRepository(environment.getWikiName())
    request = environment.getRequestMethod()

    pageName = _parsePageBaseName(environment.getPageName())
    if not pageName:
        pageName = config.defaultPage(repository.getWikiName())

    if request == "GET":
        if isSpecialPageName(pageName, "RecentChanges"):
            return DisplayRecentChanges(environment)
        if isSpecialPageName(pageName, "AllPages"):
            return DisplayAllPages(environment)

        queryDict = environment.getQueryDict()
        if queryDict.get("action", None) == ["edit"]:
            if repository.pageExists(pageName):
                return EditPage(environment)
            else:
                return EditNewPage(environment)
        elif queryDict.get("action", None) == ["history"]:
            bestMatch = repository.bestMatch(pageName)
            if bestMatch:
                return VersionHistoryPage(environment, bestMatch)
            else:
                return EditNewPage(environment)
        else:
            bestMatch = repository.bestMatch(pageName)
            if bestMatch:
                return DisplayPage(environment, bestMatch)
            else:
                return EditNewPage(environment)
    elif request == "POST":
        try:
            if environment.getFormDict()["action"] == "login":
                return Login(environment)
        except KeyError:
            pass
        return SavePage(environment)
    else:
        raise "Invalid REQUEST_METHOD: " + request


def _parsePageBaseName(fullPageName):
    elements = fullPageName.split("/")
    return elements[-1]


def isSpecialPageName(pageName, target):
    pageName = pageName.lower().replace("_", "").replace(" ", "")
    return pageName == target.lower()

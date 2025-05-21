import SessionDatabase
from Html import (
    HtmlDiv,
    HtmlForm,
    HtmlInputText,
    HtmlInputSubmit,
    HtmlPara,
    HtmlAnchor,
    HtmlInputHidden,
    H1,
)
from Config import config
from WikiPage import WikiPage, parsePageBaseName


class MightRequireLogin(WikiPage):

    def __init__(self, environment):
        WikiPage.__init__(self, environment)

    def needLogin(self):
        if not config.isYes(self.getWikiName(), "login to edit"):
            return 0

        return not SessionDatabase.isLoggedIn(self._environment.getSessionId())

    def genericLoginDiv(self, deferredAction, message=None):
        return HtmlDiv(
            id="wiki-message",
            data=HtmlForm(
                action=config.makeUrl(
                    self.getWikiName(),
                    parsePageBaseName(self._environment.getPageName()),
                ),
                normalFormatting=1,
                method="POST",
                items=[
                    HtmlInputHidden("action", "login"),
                    HtmlInputHidden("deferredAction", deferredAction),
                    HtmlPara(self.homeLink()),
                    H1("Log in"),
                    message,
                    HtmlPara(
                        [
                            "Enter your name:&nbsp;&nbsp;",
                            HtmlInputText("userName", size=50, maxLength=100),
                            "&nbsp;&nbsp;",
                            HtmlInputSubmit(" Log in "),
                        ]
                    ),
                    HtmlPara(
                        [
                            "Please enter your full name: first name and last ",
                            "name.  This will help people see which pages you've been ",
                            "working on when they click ",
                            HtmlAnchor(
                                config.makeUrl(
                                    self._environment.getWikiName(), "Recent_Changes"
                                ),
                                "Recent Changes",
                            ),
                            ".",
                        ]
                    ),
                    HtmlPara(
                        "If you'd prefer to edit anonymously, just leave the name field blank."
                    ),
                    HtmlPara("Be sure to use spaces between the words in your name."),
                ],
            ),
        )

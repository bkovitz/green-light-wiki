from teest import *
from utMisc import FakeEnvironment, resetConfig, clearSessionDict
from Misc import makeList, forceRemove

from EditPage import EditPage

from Html import Html, HtmlMeta, HtmlForm, HtmlTextArea, HtmlInputHidden, \
   HtmlInputSubmit
from VersionedFile2 import VersionedFile2
from io import StringIO
from WikiRepository import WikiRepository
from Config import config
import SessionDatabase
from Html import NoRobots

now = 1065202518


class ut_EditPage:

   def setUp(self):
      resetConfig()
      clearSessionDict()


   def testBasics(self):
      self._createFileToDisplay()

      page = EditPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageTitle",
         "George Gibbons"
      ))

      page.renderHtml()
      # no crash means pass


   def testNoRobots(self):
      self._createFileToDisplay()

      page = EditPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageTitle",
         "George Gibbons"
      ))

      pageChunk = page.renderHtml()
      TEST(NoRobots in [meta.__class__ for meta in makeList(pageChunk.metas)])


   def testEditDiv(self):
      self._createFileToDisplay()

      page = EditPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageTitle",
         "George Gibbons"
      ))

      expect = \
"""<DIV ID="wiki-edit">
  <FORM ACTION="http://greenlightwiki.com/PageTitle" METHOD=POST><TEXTAREA ROWS=24 COLS=80 WRAP=VIRTUAL NAME="text">First line
Second line
</TEXTAREA>
<DIV ID="wiki-edit-buttons">
    <INPUT TYPE=SUBMIT VALUE=" Save "><INPUT TYPE=HIDDEN NAME="origVersion" VALUE="1">
  </DIV>
</FORM>
</DIV>
"""
      TEST_EQ(str(expect), str(page.editDiv()))
      TEST_EQ("edit Page Title", page.getTitle())


   def testEditDivWithLogin(self):
      # just a test to verify that we don't crash
      config.readConfigFile(StringIO("login to edit: yes\n"))
      sessionId = SessionDatabase.makeSession(now, "128.129.130.131")
      env = FakeEnvironment(
         pathsList=["WIKI TESTWIKI/*"],
         requestMethod="GET",
         uri="/TESTWIKI/aPage",
         sessionId=sessionId,
      )

      page = EditPage(env)

      TEST_EQ(str(page.contentDiv()), str(page.loginDiv()))


   def _createFileToDisplay(self):
      forceRemove("TESTWIKI/PageTitle")

      originalText = "First line\nSecond line\n"
      wikiFile = VersionedFile2(open("TESTWIKI/PageTitle", "w+"))
      wikiFile.writeNewVersion(
         "Dr. John Mittens",
         StringIO(originalText)
      )
      wikiFile.close()

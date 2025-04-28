from teest import *
from utMisc import FakeEnvironment, forceRemove, clearSessionDict

from time import time

from SavePage import SavePage
from DisplayPage import DisplayPage

from WikiRepository import WikiRepository
from StringIO import StringIO
from Html import Html, HtmlRefresh, HtmlTextArea, NoRobots, HtmlDiv
from VersionedFile2 import VersionedFile2
import SessionDatabase
from Chunks import SuccessfulSaveChunk, CouldntSaveDueToConflictChunk, \
   EditChunk


class ut_SavePage:

   def setUp(self):
      clearSessionDict()


   def tearDown(self):
      clearSessionDict()


   def testSuccessfulSave(self):
      forceRemove("TESTWIKI/PageTitle")

      sessionId = SessionDatabase.makeSession(time(), "128.129.130.131")

      page = SavePage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageTitle",
         "George Gibbons",
         StringIO("First line\r\n\r\nSecond line\r\n"),
         formDict={"origVersion": "0"},
         sessionId = sessionId
      ))
      page.action()

      # check the redirect

      got = page.renderCgi()
      TEST(got.find("Status: 303\n") >= 0)
      TEST(got.find("Location: http://greenlightwiki.com/PageTitle\n") >= 0)

      # TODO: check the pending message

      messageChunkClass, pageName = \
         SessionDatabase.getPendingMessage(sessionId)
      TEST_EQ(SuccessfulSaveChunk, messageChunkClass)
      TEST_EQ(("Page Title",), pageName)

      # check that the file was actually saved

      newFile = file("TESTWIKI/PageTitle", "r")
      expect = ["First line\n", "\n", "Second line\n"]
      versionedFile = VersionedFile2(newFile)
      got = versionedFile.getVersion(1)
      TEST_EQ(expect, got)

      # now check that the DisplayPage shows a confirmation message

      page = DisplayPage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageTitle",
         "George Gibbons",
         sessionId = sessionId
      ))
      page.makeData()

      TEST_EQ(
         SuccessfulSaveChunk(page, "Page Title", WikiRepository("TESTWIKI")),
         page.getBody().message
      )


   def testFailToSavePage(self):
      forceRemove("TESTWIKI/PageTitle")

      originalText = "The first version of this file.\n"
      wikiFile = VersionedFile2(file("TESTWIKI/PageTitle", "w+"))
      wikiFile.writeNewVersion(
         "Dr. John Mittens",
         StringIO(originalText)
      )
      wikiFile.close()

      page = SavePage(FakeEnvironment(
         WikiRepository("TESTWIKI"),
         "PageTitle",
         "George Gibbons",
         StringIO("Some text\nthat won't get saved\n"),
         formDict={"origVersion": "0"}
      ))
      page.action()

      # check that there is *not* a redirect

      got = page.renderCgi()
      TEST(got.find("Status: 303\n") < 0)


      #expect = Html("Conflicting edits on Page Title")
      #expect.addHeadItem([
         #noRobots()
      #])

      # check "failed to save" message

      body = page.getBody()

      TEST_EQ(
         CouldntSaveDueToConflictChunk(
            page,
            "PageTitle",
            "Dr. John Mittens",
            WikiRepository("TESTWIKI")
         ),
         body.message
      )

      # check the content area

      TEST_EQ(
         EditChunk(page, "Some text\nthat won't get saved\n"),
         body.content
      )

      # check the page file

      wikiFile = VersionedFile2(file("TESTWIKI/PageTitle", "r"))
      TEST_EQ(1, wikiFile.getLatestVersionNum())
      TEST_EQ([originalText], wikiFile.getLatestVersion())
      wikiFile.close()

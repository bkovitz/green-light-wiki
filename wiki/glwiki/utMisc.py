from teest import *
from HtmlMisc import metaKeywords

import os, cgi
from StringIO import StringIO
from Config import config
from File import File
from Environments import Environment
from PathMatch import PathMatch
from Misc import forceRemove
import SessionDatabase


class NonexistentFile(File):

   def __init__(self, filename=None):
      self.filename = filename
      self._f = None
      self._exists = 0


class FileFromList(File):

   def __init__(self, lis, filename=None):
      self.filename = filename
      self._f = StringIO("\n".join(lis))
      self._exists = 1


class FileFromString(File):

   def __init__(self, s):
      self.filename = ""
      self._f = StringIO(s)
      self._exists = 1


class UncloseableStringIO(StringIO):

   def close(self):
      pass


class FakePageFile:

   def __init__(self, fileContents, filename="TESTDATA/FakeFile"):
      self.fakeFile = UncloseableStringIO(
"""
@@ version 1; date 2003.7.24.10.36.01; author GeorgeGibbons;
""" + fileContents)
      self.filename = filename


   def openForReading(self):
      return self.fakeFile


   def openForWriting(self):
      return file(self.filename, "w+")


def resetConfig():
   config.readConfigFile(file("wiki.config", "r"))


def clearSessionDict():
   forceRemove("wiki.sessions")
   forceRemove("wiki.messages")


class FakeEnvironment(Environment):

   def __init__(
      self,
      repository=None,
      pageName=None,
      userName=None,
      inputFile=None,
      formDict=None,
      sessionId=None,
      pathsList=None,
      requestMethod=None,
      queryString=None,
      wikiName=None,
      uri=None,
      httpHost=None
   ):
      self._commandLine = None
      self._environ = None

      self._requestUri = uri
      self._httpHost = httpHost
      if pathsList:
         self._pathMatch = PathMatch(FileFromList(pathsList))
         self._extractPathInfo()
      else:
         if repository:
            self._wikiName = repository.getWikiName()
         else:
            self._wikiName = wikiName
         self._pageName = pageName

      self._requestMethod = requestMethod
      if queryString:
         self._queryDict = cgi.parse_qs(queryString)
      else:
         self._queryDict = {}
      self._formDict = formDict
      self._userName = userName
      self._inputFile = inputFile
      self._sessionId = sessionId
      self._ipAddress = "128.129.130.131"


def DEBUG(obj, prefix="***"):
   print "%s (class=%s)" % (prefix, obj.__class__.__name__)
   for elem in dir(obj):
      try:
         print "   %s = %s" % (elem, repr(obj.__dict__[elem]))
      except:
         pass


class ut_testMisc:

   def testKeywords(self):
      resetConfig()
      expect = '<META NAME="keywords" CONTENT="wiki, green light wiki, unit test">\n'
      got = metaKeywords("fakeWikiName")

      TEST_EQ(expect, str(got))

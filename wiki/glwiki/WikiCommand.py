import re, cgi
from io import StringIO
from CgiEnvironment import CgiEnvironment


def makeWikiCommandFromApacheEnvironment(environ, stdin=None, wikiName=None):
   command = inputFile = targetString = None
   environ = CgiEnvironment(environ)

   targetString = environ.get("REDIRECT_URL")
   formDict = None

   if wikiName:
      pageName = _lastElementAfterSlash(targetString)
   else:
      wikiName = _extractWikiName(targetString)
      pageName = _extractPageName(targetString)

   request = environ.get("REQUEST_METHOD")
   if request == "GET":
      if pageName.endswith(".html"):  #TODO: get rid of this
         command = "STATIC"
      else:
         queryString = cgi.parse_qs(environ.get("QUERY_STRING"))
         if queryString.get("action", None) == ["edit"]:
            command = "EDIT"
         else:
            command = "DISPLAY"
   elif request == "POST":
      command = "SAVE"
      formDict = _getDictFromStdin(stdin)
      inputFile = StringIO(formDict["text"])

   return WikiCommand(
      command,
      wikiName,
      pageName,
      inputFile,
      environ.get("REMOTE_ADDR"),
      formDict
   )


def getWikiNameFromApacheEnvironment(environ):
   return _extractWikiName(environ.get("REDIRECT_URL"))


def getPageNameFromApacheEnvironment(environ):
   return _extractPageName(environ.get("REDIRECT_URL"))


class WikiCommand:

   def __init__(
      self,
      command,
      wikiName,
      pageName,
      inputFile=None,
      userName=None,
      formDict=None,
   ):
      self.command = command
      self.wikiName = wikiName
      self.pageName = pageName
      self.inputFile = inputFile
      self.userName = userName
      self.formDict = formDict


   def origVersion(self):
      if self.formDict:
         return self.formDict.get("origVersion", 0)
      else:
         return 0


   def __eq__(self, other):
      return (
         self.command == other.command
         and
         self.wikiName == other.wikiName
         and
         self.pageName == other.pageName
         and
         self.userName == other.userName
         and
         self.formDict == other.formDict
      )


   def __ne__(self, other):
      return not self == other


def _extractWikiName(url):
   try:
      return _extractElements(url)[0]
   except IndexError:
      return ""


def _extractPageName(url):
   elements = _extractElements(url)
   if len(elements) >= 2:
      return elements[-1]
   else:
      return ""


def _lastElementAfterSlash(url):
   elements = re.split("/", url)
   if len(elements) == 0:
      return ""
   else:
      return elements[-1]


def _extractElements(url):
   allElements = re.split("/", url)
   return filter(_isNotJunkElement, allElements)


def _isNotJunkElement(element):
   return (
      element != ""
      and
      element[-1] != ":"
   )


def _getDictFromStdin(stdin):
   result = {}
   for line in stdin.readlines():
      d = cgi.parse_qs(line.rstrip())
      for key in d.keys():
         if key not in result:
            result[key] = d[key][0]

   return result

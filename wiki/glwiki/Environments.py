#import cgi, urllib
#from StringIO import StringIO
from io import StringIO
#from Cookie import SimpleCookie
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, unquote

from PathMatch import PathMatch
from PageFactories import getPageFactory
import SessionDatabase

def getEnvironment(commandLine, environ, pathsFile, stdin):
   return ApacheEnvironment(commandLine, environ, pathsFile, stdin)


class Environment:

   def __init__(
      self,
      commandLine,
      environ,
      pathMatch,
      requestMethod,
      queryString,
      requestUri,
      httpHost,
      formDict,
      userName,
      ipAddress,
      inputFile,
      cookies,
      sessionId=None
   ):
      self._commandLine = commandLine
      self._environ = environ
      self._pathMatch = pathMatch
      self._requestMethod = requestMethod
      #self._queryDict = cgi.parse_qs(queryString)
      self._queryDict = parse_qs(queryString)
      self._requestUri = requestUri
      self._httpHost = httpHost
      self._formDict = formDict
      self._userName = userName
      self._ipAddress = ipAddress
      self._inputFile = inputFile
      self._extractPathInfo()
      self._cookies = cookies
      self._sessionId = sessionId

      self._requestedPage = getPageFactory(self._fileType)(self)


   def _extractPathInfo(self):
      self._wikiName, self._fileType, self._pageName = \
         self._pathMatch.pathInfo(self.getUri(), self.getHttpHost())
      #self._pageName = urllib.unquote(self._pageName)
      self._pageName = unquote(self._pageName)


   def getRequest(self):       return self._requestMethod
   def getQueryDict(self):     return self._queryDict
   def getUri(self):           return self._requestUri
   def getHttpHost(self):      return self._httpHost
   def getRequestedPage(self): return self._requestedPage
   def getWikiName(self):      return self._wikiName
   def getPageName(self):      return self._pageName
   def getRequestMethod(self): return self._requestMethod
   def getIpAddress(self):     return self._ipAddress
   def getFormDict(self):      return self._formDict
   def getInputFile(self):     return self._inputFile
   def getSessionId(self):     return self._sessionId

   def getCookie(self, cookieName):
      try:
         return self._cookies[cookieName].value
      except KeyError:
         return None


   def getUserName(self):
      result = SessionDatabase.getUserName(self.getSessionId())
      if result == "(unknown)":
         return self.getIpAddress()
      else:
         return result



class ApacheEnvironment(Environment):
   
   def __init__(self, commandLine, environ, pathsFile, stdin):
      formDict = _getDictFromStdin(stdin)
      if "text" in formDict:
         inputFile = StringIO(formDict["text"])
      else:
         inputFile = StringIO()

      cookies = SimpleCookie()
      try:
         cookies.load(environ["HTTP_COOKIE"])
      except KeyError:
         pass

      ipAddress = environ.get("REMOTE_ADDR")

      userName = self._extractUserName(cookies, ipAddress)

      Environment.__init__(
         self,
         commandLine,
         environ,
         PathMatch(pathsFile),
         environ.get("REQUEST_METHOD", ""),  #TODO: throw exc
         environ.get("QUERY_STRING", ""),
         environ.get("REQUEST_URI", ""),  #TODO: throw exc
         environ.get("HTTP_HOST", ""),  #TODO: throw exc
         formDict,
         userName,
         ipAddress,
         inputFile,
         cookies,
         _extractSessionId(cookies)
      )


   def _extractUserName(self, cookies, ipAddress):
      sessionId = _extractSessionId(cookies)
      return SessionDatabase.getUserName(sessionId)


def _extractSessionId(cookies):
   try:
      result = cookies["wiki-session"].value
   except KeyError:
      return None

   if result.endswith(","):
      result = result[:-1]

   return result


def _getDictFromStdin(stdin):
   result = {}
   for line in stdin.readlines():
      #d = cgi.parse_qs(line.rstrip())
      d = parse_qs(line.rstrip())
      for key in d.keys():
         if key not in result:
            result[key] = d[key][0]

   return result

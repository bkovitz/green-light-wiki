import re, os.path

from Config import config
from Misc import stripLeadingSlash

bad = "BAD"
wiki = "WIKI"
static = "STATIC"
plain = "PLAIN"

class PathMatch:

   def __init__(self, _pathsFile):
      self._pathsFile = _pathsFile


   def pathInfo(self, path, httpHost=None):
      path = _stripJunk(path)

      if not self._pathsFile.exists():
         if "/" not in path:
            return "", "WIKI", path
         else:
            return "", "BAD", path

      for pathLine in self._pathsFile:
         hostName, wikiName, fileType, pathWithWildcards = \
            _parsePathLine(pathLine)
         pathWithWildcards = stripLeadingSlash(pathWithWildcards)

         if hostName is not None and httpHost is not None:
            if hostName != httpHost:
               continue

         #TODO: make the code below more readable
         if fileType:
            regexp = _convertToRegexp(pathWithWildcards)

            if re.match(regexp, path):
               return wikiName, fileType.upper(), path

            defaultPage = _appendSlash(path) + \
               _defaultPageForFileType(fileType, wikiName)
            if (
               re.match(regexp, defaultPage)
               #and
               #os.path.exists(config.getNonwikiFilename(defaultPage))
            ):
               return wikiName, fileType.upper(), defaultPage

            defaultPage = path + _defaultPageForFileType(fileType, wikiName)
            if (
               pathWithWildcards == "*"
               and
               re.match(regexp, defaultPage)
               #and
               #os.path.exists(config.getNonwikiFilename(defaultPage))
            ):
               return wikiName, fileType.upper(), defaultPage

      return "", "BAD", path
         

def _stripJunk(uri):
   return _stripQueryString(stripLeadingSlash(uri))


def _stripQueryString(uri):
   index = uri.find("?")
   if index >= 0:
      uri = uri[:index]
   return uri


_pathElements = "((?://)|(?:/)|(?:\*)|(?:[^/*]+))"

_pathElementsDict = {
   "/": "/",
   "*": "[^/]+",
   "//": "/(.+/)*",
}

def _convertToRegexp(pathWithWildcards):
   result = ""
   gotADoubleSlash = 0
   for element in re.findall(_pathElements, pathWithWildcards):
      if element in _pathElementsDict:
         result += _pathElementsDict[element]
      else:
         result += re.escape(element)

   return result + "$"


def _parsePathLine(pathLine):
   words = pathLine.strip().split(" ")
   if len(words) < 2 or len(words) > 3:
      return None, None, None, None
   if words[0] == "WIKI":
      if len(words) == 3:
         host, path = _parseHostAndPath(words[2])
         return host, words[1], "WIKI", path
      else:
         assert len(words) == 2
         host, path = _parseHostAndPath(words[1])
         return host, _defaultWikiName(words[1]), "WIKI", path
   else:
      if len(words) == 2:
         host, path = _parseHostAndPath(words[1])
         return host, "", words[0], path
      else:
         return None, None, None, None


def _defaultWikiName(path):
   pathElements = path.split("/")
   if len(pathElements) <= 1:
      return ""
   else:
      return pathElements[-2]


parseHostAndPathRE = re.compile("http://(?P<host>.+?)/(?P<path>.*)")
def _parseHostAndPath(spec):
   m = parseHostAndPathRE.match(spec)
   if m is not None:
      dict = m.groupdict()
      return dict.get("host", None), dict.get("path", None)
   else:
      return None, spec


def _defaultPageForFileType(fileType, wikiName):
   if fileType == "WIKI":
      return config.defaultPage(wikiName)
   else:
      return "index.html"


def _appendSlash(path):
   if not path or path[-1] == "/":
      return path
   else:
      return path + "/"

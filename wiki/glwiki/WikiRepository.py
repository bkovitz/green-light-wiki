import os, os.path, time
from fcntl import lockf, LOCK_EX, LOCK_SH
#from urllib import quote
from urllib.parse import quote

from Config import config
from UnsmashWords import unsmashWords


class PageFile:
   """
      We lock all files for the entire duration that they're open.  Caller
      must close file or lock will persist indefinitely.
   """

   def __init__(self, fullPath):
      self.fullPath = fullPath


   def openForReading(self):
      try:
         #result = open(self.fullPath, "r")
         result = open(self.fullPath, "r", errors='ignore')
         lockf(result, LOCK_SH)
         return result
      except IOError:
         return None


   def openForWriting(self):
      try:
         result = open(self.fullPath, "r+", errors='ignore')
      except IOError:
         result = open(self.fullPath, "w+", errors='ignore')
      lockf(result, LOCK_EX)
      return result


   def openForAppending(self):
      result = open(self.fullPath, "a+", errors='ignore')
      lockf(result, LOCK_EX)
      return result


   def getModificationTime(self):
      mtime = os.stat(self.fullPath).st_mtime
      return time.gmtime(mtime)[:6]


class WikiRepository:

   def __init__(self, directory):
      self.directory = directory


   def makeUrl(self, pageName):
      return config.get(self.directory, "url prefix", "/") + quote(pageName, "")


   def pageExists(self, pageName):
      return os.path.exists(self._path(pageName))


   def pageFile(self, pageName):
      return PageFile(self._path(pageName))


   def recentChangesFilename(self):
      return self.directory + ".RecentChanges"


   def allPageNames(self):
      return [
         filename
            for filename in os.listdir(self.directory)
               if os.path.isfile(self.directory + "/" + filename)
      ]


   def getWikiName(self):
      return self.directory


   def bestMatch(self, pageName):
      return _bestMatch(self.allPageNames(), pageName)


   def closePageExists(self, pageName):
      return _bestMatch(self.allPageNames(), pageName) != None


   def _path(self, pageName):
      return os.path.normpath(self.directory + "/" + pageName)


class NullRepository(WikiRepository):

   def __init__(self):
      self.directory = ""


   def pageExists(self, pageName):
      return 0


def _bestMatch(names, target):
   best = None
   unsmashedTarget = unsmashWords(target)

   for name in names:
      if name == target:
         return name

      if name == unsmashedTarget:
         best = name
         continue

      if name.lower() == target.lower():
         best = name
         continue

      if unsmashWords(name) == unsmashedTarget:
         best = name
         continue

      if unsmashWords(name).lower() == unsmashedTarget.lower():
         best = name
         continue

   return best

import re, sys

class Config:

   hasCommentRE = re.compile("^\s*#")
   parseRE = re.compile("\s*(?P<name>.*?)\s*:\s*(?P<value>.*)\s*")


   def __init__(self, configFile):
      self.readConfigFile(configFile)


   def readConfigFile(self, configFile):
      self.dict = {}

      self.wikiName = ""
      for line in configFile.readlines():
         line = self._stripComments(line)
         if len(line) > 0:
            self._parseLine(line)

      
   def get(self, wikiName, key, default=""):
      if (wikiName, key) in self.dict:
         return self.dict.get((wikiName, key))
      else:
         return self.dict.get(("", key), default)


   def isYes(self, wikiName, key):
      try:
         value = self.dict[(wikiName, key)]
      except KeyError:
         try:
            value = self.dict[("", key)]
         except KeyError:
            value = "n"

      return value[0].upper() == "Y"


   def makeUrl(self, wikiName, pageName):
      return self.get(wikiName, "url prefix") + pageName


   def homeUrl(self, wikiName):
      return self.makeUrl(wikiName, self.defaultPage(wikiName))


   def titleFontStart(self, wikiName):
      return self.get(
         wikiName,
         "title font start",
         "<FONT FACE=Tahoma,Helvetica,Arial COLOR=#CC3399 SIZE=6><B>"
      )


   def titleFontEnd(self, wikiName):
      return self.get(
         wikiName,
         "title font end",
         "</B></FONT>"
      )


   def noticeFontStart(self, wikiName):
      return self.get(
         wikiName,
         "notice font start",
         "<FONT FACE=Tahoma,Helvetica,Arial COLOR=#CC3399 SIZE=2>"
      )


   def noticeFontEnd(self, wikiName):
      return self.get(
         wikiName,
         "notice font end",
         "</FONT>"
      )


   def logo(self, wikiName):
      return self.get(wikiName, "logo file")


   def defaultPage(self, wikiName):
      return self.get(wikiName, "default page", "WelcomePage")


   def pageFilename(self):
      path = env.wikiDir()
      if len(path) == 0:
         return env.pageName()
      else:
         return os.normpath(path + "/" + env.pageName())


   def _stripComments(self, line):
      if self.hasCommentRE.match(line) != None:
         return ""
      return line.rstrip()


   def _parseLine(self, line):
      words = re.split('\s+', line)
      if len(words) >= 2 and words[0] == "WIKI":
         self.wikiName = words[1]
      else:
         matchObject = self.parseRE.match(line)
         matches = matchObject.groupdict()
         self.dict[(self.wikiName, self._fix(matches["name"]))] = \
            self._fix(matches["value"])


   def _fix(self, s):
      return s.strip()


   def getNonwikiFilename(self, uriPath):
      uriPath = stripLeadingSlash(uriPath)

      baseDir = self.get("", "base directory")
      if not baseDir:
         return uriPath

      if baseDir[-1] != "/":
         baseDir += "/"

      return baseDir + uriPath


#config = Config(file("wiki.config", "r"))
config = Config(open("wiki.config", "r"))


# OAOO: also in Misc
def stripLeadingSlash(uri):
   if uri and uri[0] == "/":
      return uri[1:]
   else:
      return uri

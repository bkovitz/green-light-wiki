#from HTMLParser import HTMLParser
from html.parser import HTMLParser

class BodyExtractor(HTMLParser):

   def __init__(self, inputFile):
      HTMLParser.__init__(self)
      self.inputFile = inputFile
      self.reset()


   def body(self):
      if not self._body:
         self._readEverything()
      return self._body


   def title(self):
      if not self._title:
         self._readEverything()
      return self._title


   def links(self):
      if not self._body:
         self._readEverything()
      return self._links


   def cgiLeader(self):
      if not self._body:
         self._readEverything()
      return self._cgiLeader


   def reset(self):
      self._body = ""
      self._title = ""
      self._links = []
      self._cgiLeader = []
      self._inCgiLeader = 1
      self.inBody = 0
      self._inTitle = 0
      HTMLParser.reset(self)


   def _readEverything(self):
      self.reset()
      for line in self.inputFile:
         if self._inCgiLeader and line.rstrip() and not line.startswith("<"):
            self._cgiLeader.append(line.rstrip())
         else:
            self._inCgiLeader = 0
            self.feed(line)


   def handle_starttag(self, tag, attrs=None):
      if self.inBody:
         self._body += self.get_starttag_text()

      if tag.upper() == "HTML":
         self._inHtml = 1
      elif tag.upper() == "BODY":
         self.inBody = 1
      elif tag.upper() == "TITLE":
         self._inTitle = 1
      elif tag.upper() == "LINK":
         self._links.append(self.get_starttag_text())


   def handle_endtag(self, tag):
      if tag.upper() == "BODY":
         self.inBody = 0
      elif tag.upper() == "TITLE":
         self._inTitle = 0

      if self.inBody:
         self._body += "</%s>" % tag.upper()


   def handle_data(self, data):
      if self.inBody:
         self._body += self.mungeData(data)
      elif self._inTitle:
         self._title += data


   def mungeData(self, data):
      return data   # override to modify data on the fly


   def handle_entityref(self, name):
      if self.inBody:
         self._body += "&%s;" % name
      elif self._inTitle:
         self._title += name


   def handle_charref(self, name):
      if self.inBody:
         self._body += "&#%s;" % name
      elif self._inTitle:
         self._title += name

from HTMLParser import HTMLParser
from Html import Html

class HtmlReader(HTMLParser):

   def __init__(self, inputFile):
      HTMLParser.__init__(self)
      self.inputFile = inputFile


   def extract(self):
      self.reset()
      for line in self.inputFile:
         self.feed(line)
      return self.html


   def reset(self):
      HTMLParser.reset(self)
      self.html = Html()
      self.inBody = 0
      self.inHead = 0


   def handle_starttag(self, tag, attrs=None):
      tag = tag.upper()

      if tag == "BODY":
         self.inBody = 1
         self.inHead = 0
      elif tag == "HEAD":
         self.inBody = 0
         self.inHead = 1
      else:
         self.add(self.get_starttag_text())


   def handle_endtag(self, tag):
      tag = tag.upper()

      if tag == "BODY":
         self.inBody = 0
      elif tag == "HEAD":
         self.inHead = 0
      else:
         self.add("</%s>" % tag.upper())
         

   def add(self, item):
      if self.inBody:
         self.html.add(item)
      elif self.inHead:
         self.html.addHeadItem(item)


   def handle_data(self, data):
      self.add(data)


   def handle_entityref(self, name):
      self.add("&%s;" % name)


   def handle_charref(self, name):
      self.add("&#%s;" % name)

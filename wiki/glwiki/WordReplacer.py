import re
from curses.ascii import ispunct

from WikiRepository import NullRepository
from Html import Class, HtmlAnchor, HtmlImage
from LatexImage import LatexImage

_wordTypes = "((?:\$\$.+?\$\$)|(?:\[\[.+?\]\])|(?:http://\S+)|(?:ftp://\S+)|(?:https://\S+)|(?:mailto:\S+)|(?:\<)|(?:\>)|(?:\&)|(?:\w+)|(?:\s+)|(?:-{4,})|(?:''')|(?:'')|(?:[^\w\s]))"

_externalClass = Class("external")
_newClass = Class("new")

class WordReplacer:

   def __init__(self, repository=None):
      if repository == None:
         self.repository = NullRepository()
      else:
         self.repository = repository

      self.italics = 0
      self.bold = 0


   def replaceWords(self, line):
      return "".join([str(o) for o in self.replaceWordsWithObjects(line)])


   def replaceWordsWithObjects(self, line):
      return [ self._replaceWord(w) for w in self.allWords(line) ]


   def allWords(self, line):
      return re.findall(_wordTypes, line.strip())


   def _replaceWord(self, word):
      if word[0:4] == "----":
         return "<HR>"
      elif word[0:7] == "http://":
         return self._httpLink(word)
      elif word.startswith("ftp://"):
         return self._ftpLink(word)
      elif word.startswith("https://"):
         return self._httpsLink(word)
      elif word[0:7] == "mailto:":
         return self._mailtoLink(word)
      elif word.startswith("[[") and word.endswith("]]"):
         return self._bracketLink(word[2:-2])
      elif word == "<":
         return "&lt;"
      elif word == ">":
         return "&gt;"
      elif word == "&":
         return "&amp;"
      elif word.isspace():
         return " "
      elif word == "''":
         return self._toggleItalics()
      elif word == "'''":
         return self._toggleBold()
      elif word.startswith("$$") and word.endswith("$$") and len(word) > 4:
         return LatexImage(self.repository, word[1:-1])
      else:
         return word


   def _bracketLink(self, betweenTheBrackets):
      words = betweenTheBrackets.split()
      url = ""
      class_ = None
      labelWords = []

      for word in words:
         if (
            word[0:7] == "http://"
            or
            word.startswith("ftp://")
            or
            word.startswith("https://")
         ):
            url = word
            class_ = _externalClass
         else:
            labelWords.append(word)

      if url == "":
         targetPage = "_".join(labelWords)
         url = self.repository.makeUrl(targetPage)
         if not self.repository.closePageExists(targetPage):
            class_ = _newClass

      return makeAnchor(
         url,
         " ".join(labelWords),
         class_
      )


   def _httpLink(self, httpWord):
      lastChar = httpWord[-1]
      if ispunct(lastChar) and lastChar != "/":
         word = httpWord[0:-1]
         return makeRemoteLink(word) + lastChar
      else:
         return makeRemoteLink(httpWord)


   def _ftpLink(self, ftpWord):
      lastChar = ftpWord[-1]
      if ispunct(lastChar) and lastChar != "/":
         word = ftpWord[0:-1]
         return makeRemoteLink(word) + lastChar
      else:
         return makeRemoteLink(ftpWord)


   def _httpsLink(self, httpsWord):
      lastChar = httpsWord[-1]
      if ispunct(lastChar) and lastChar != "/":
         word = httpsWord[0:-1]
         return makeRemoteLink(word) + lastChar
      else:
         return makeRemoteLink(httpsWord)


   def _mailtoLink(self, mailtoWord):
      lastChar = mailtoWord[-1]
      if ispunct(lastChar):
         word = mailtoWord[0:-1]
         return makeAnchor(word, word, _externalClass) + lastChar
      else:
         return makeAnchor(mailtoWord, mailtoWord, _externalClass)


   def _toggleItalics(self):
      if not self.italics:
         self.italics = 1
         return "<EM>"
      else:
         self.italics = 0
         return "</EM>"


   def _toggleBold(self):
      if not self.bold:
         self.bold = 1
         return "<STRONG>"
      else:
         self.bold = 0
         return "</STRONG>"


   def _hasForcedLineBreak(self, line):
      return len(line) > 0 and line[0] == " "


   def _localFilename(self, basename):
      return os.path.join(
         config.get(self.repository.getWikiName(), "file directory"),
         os.path.basename(basename)
      )


def makeAnchor(url, text, attrs=None):
   return str(HtmlAnchor(url, text, attrs))


def makeRemoteLink(url):
   if url.endswith(".gif") or url.endswith(".jpg") or url.endswith(".jpeg"):
      return str(HtmlImage(url))
   else:
      return str(makeAnchor(url, url, _externalClass))



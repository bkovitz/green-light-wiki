import re, os.path
from types import StringType, ListType
from curses.ascii import ispunct

from Html import HtmlAnchor, HtmlUnorderedList, HtmlListItem, HtmlHolder, \
                 ListRow, HtmlImage, HtmlOrderedList, HtmlPara, Class, Hn
from Config import config
from WikiRepository import NullRepository
from BodyExtractor import BodyExtractor
from UnsmashWords import unsmashWords
from LatexImage import LatexImage
import RecentChanges

bullet = "&#149;"

# parser states
ST_START = 0
ST_IN_UNORDERED_LIST = 1
ST_IN_ORDERED_LIST = 2

_wordTypes = "((?:\$\$.+?\$\$)|(?:\{\{.+\}\})|(?:\[\[.+?\]\])|(?:http://\S+)|(?:ftp://\S+)|(?:https://\S+)|(?:mailto:\S+)|(?:\<)|(?:\>)|(?:\&)|(?:\w+)|(?:\s+)|(?:-{4,})|(?:''')|(?:'')|(?:[^\w\s]))"
_matchAllTextAfterHyphens = "-+\s*(?P<after>.*)$"
_parseHeading = "(?P<before>=+)(?P<between>.*?)(?P<after>=+)$"

_externalClass = Class("external")
_newClass = Class("new")

_equalsDict = {
   "=":     1,
   "==":    2,
   "===":   3,
   "====":  4,
   "=====": 5,
}


class WikiTextException(Exception):
   pass

_wikiTextException = WikiTextException()


def assume(cond):
   if not cond:
      raise _wikiTextException


def isBlank(s):
   return (
      (
         type(s) == StringType
         or
         type(s) == ListType
      )
      and
      len(s) == 0
   )


class WikiTextParser:
   
   def __init__(self, result, wordReplacer):
      self._result = result;
      self._itemInProgress = None
      self._wordReplacer = wordReplacer

      self._parseMethods = [
         self._paragraphBreak,
         self._horizontalRule,
         self._forcedLineBreak,
         self._heading,
         self._bulletedListItem,
         self._numberedListItem,
         self._replaceWords,
         self._plainItem,
      ]


   def feedLine(self, line):
      self._setLine(line)

      for parseMethod in self._parseMethods:
         self._keepGoing = 0
         try:
            parseMethod(self._line)
            if not self._keepGoing:
               break
         except (WikiTextException, AttributeError, IndexError, TypeError):
            continue


   def _plainItem(self, item):
      assume(not isBlank(item))

      if not self._itemInProgress or self._inList():
         self._itemInProgress = HtmlPara()  #TODO: _newItemInProgress
         self._result.append(self._itemInProgress)

      self._itemInProgress.add(item)
      if type(item) == StringType:
         self._itemInProgress.add("\n")


   def _paragraphBreak(self, item):
      assume(isBlank(item) and not self._inList())
      self._itemInProgress = None


   def _horizontalRule(self, item):
      assume(item.startswith("----"))
      self._itemInProgress = None
      self._result.append("<HR>\n")
      self._setLine(_textAfterHyphens(item))


   def _heading(self, item):
      m = re.match(_parseHeading, item)

      heading = m.groupdict()
      before = heading["before"]
      after = heading["after"]

      assume(self._isHeading(before, after))

      tag = Hn(
         _equalsDict[before],
         self._wordReplacer.replaceWords(heading["between"].strip())
      )

      self._itemInProgress = None
      self._result.append(tag)


   def _forcedLineBreak(self, item):
      assume(item[0] == " ") #TODO: startswith
      if self._itemInProgress:
         self._itemInProgress.add("<BR>\n")  #TODO: make a tag
      self._setLine(item.lstrip())


   def _bulletedListItem(self, item):
      assume(item.startswith("*"))
      if self._itemInProgress.__class__ != HtmlUnorderedList:
         self._newItemInProgress(HtmlUnorderedList())
      self._itemInProgress.add(
         HtmlListItem(self._wordReplacer.replaceWords(item[1:].strip()))
      )


   def _numberedListItem(self, item):
      assume(item.startswith("#"))
      if self._itemInProgress.__class__ != HtmlOrderedList:
         self._newItemInProgress(HtmlOrderedList())
      self._itemInProgress.add(
         HtmlListItem(self._wordReplacer.replaceWords(item[1:].strip()))
      )


   def _replaceWords(self, item):
      self._setLine(self._wordReplacer.replaceWords(item))


   def _newItemInProgress(self, newItem):
      self._itemInProgress = newItem
      self._result.append(newItem)


   def _isHeading(self, before, after):
      return (
         before in _equalsDict
         and
         after in _equalsDict
         and
         before == after
      )


   def _setLine(self, line):
      try:
         self._line = line.rstrip()
      except AttributeError:
         self._line = line
      self._keepGoing = 1


   def _inList(self):
      if not self._itemInProgress:
         return 0
      itemClass = self._itemInProgress.__class__
      return (
         itemClass == HtmlUnorderedList
         or
         itemClass == HtmlOrderedList
      )


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
      elif word.startswith("{{") and word.endswith("}}"):
         return self._execute(word)
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


   def _execute(self, word):
      cmd = word[2:-2].strip()  # strip braces
      if cmd.endswith(".html"):
         extractor = BodyExtractor(file(self._localFilename(cmd)))
         result = extractor.body()
         del extractor
         return result
      elif cmd == "RecentChanges":
         return RecentChanges.render(self.repository.recentChangesFilename())
      else:
         return word


   def _hasForcedLineBreak(self, line):
      return len(line) > 0 and line[0] == " "


   def _localFilename(self, basename):
      return os.path.join(
         config.get(self.repository.getWikiName(), "file directory"),
         os.path.basename(basename)
      )


class WikiText:

   def __init__(self, text, repository=None):
      self.text = text
      self._repository = repository

      if repository == None:
         self.repository = NullRepository()
      else:
         self.repository = repository

      self.italics = 0
      self.bold = 0


   def renderParas(self):
      result = []
      parser = WikiTextParser(result, WordReplacer(self._repository))

      for line in self.text:
         parser.feedLine(line)

      return result


   def renderHtml(self):
      return "".join([str(para) for para in self.renderParas()])


def makeAnchor(url, text, attrs=None):
   return str(HtmlAnchor(url, text, attrs))


def makeRemoteLink(url):
   if url.endswith(".gif") or url.endswith(".jpg") or url.endswith(".jpeg"):
      return str(HtmlImage(url))
   else:
      return str(makeAnchor(url, url, _externalClass))


def _hasForcedLineBreak(line):
   return len(line) > 0 and line[0] == " "


def _textAfterHyphens(line):
   match = re.match(_matchAllTextAfterHyphens, line)
   if match:
      return match.groupdict()["after"]

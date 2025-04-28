import re, os.path
#from types import StringType, ListType

from WordReplacer import WordReplacer
from WikiRepository import NullRepository

from Chunks import ParagraphChunk, Heading1Chunk, Heading2Chunk, \
   Heading3Chunk, Heading4Chunk, Heading5Chunk, UnorderedListItemChunk, \
   OrderedListItemChunk
from Paragraphs import Paragraph

_parseHeading = "(?P<before>=+)(?P<between>.*?)(?P<after>=+)$"

_heading1RE = re.compile("^={1,5}[^=].*={1,5}$")

_headingChunks = [
   Heading1Chunk,
   Heading2Chunk,
   Heading3Chunk,
   Heading4Chunk,
   Heading5Chunk,
]


class WikiTextException(Exception):
   pass

_wikiTextException = WikiTextException()


def assume(cond):
   if not cond:
      raise _wikiTextException


def isBlank(s):
   return (
      (
#         type(s) == StringType
#         or
#         type(s) == ListType
          isinstance(s, (str, list))
      )
      and
      len(s) == 0
   )


ST_START = 0
ST_GOT_LINE_BREAK = 1

class ParagraphChunkList:

   def __init__(self):
      self._list = []


   def addPara(self, para):
      self._list.append(para)


   def coalescePara(self, para):
      try:
         self._list[-1].coalesceWith(para)
      except IndexError:
         self.addPara(para)


   def getList(self):
      return self._list


class WikiText2:

   def __init__(self, text, repository=None):
      self.text = text

      if repository == None:
         self._repository = NullRepository()
      else:
         self._repository = repository

      self._replacer = WordReplacer(self._repository)


   def renderParas(self, page):
      return [
         para.makeChunk(page)
            for para in self.makeParas()
      ]


   def makeParas(self):
      initialParas = [
         self._makePara(para)
            for para in _parseParas(self.text)
      ]

      result = ParagraphChunkList()
      state = ST_START
      for para in initialParas:
         if state == ST_START:
            if para.__class__ == LineBreak:
               state = ST_GOT_LINE_BREAK
            else:
               result.addPara(para)
         elif state == ST_GOT_LINE_BREAK:
            result.coalescePara(para)
            state = ST_START

      return result.getList()


   def _makePara(self, para):
      if para.__class__ == LineBreak:
         return para
      elif self._isHeading(para):
         return Paragraph(
            self._headingChunk(para),
            self._renderWikiText(self._headingText(para))
         )
      elif self._isUnorderedListItem(para):
         return Paragraph(
            UnorderedListItemChunk,
            self._renderWikiText(para[2:])
         )
      elif self._isOrderedListItem(para):
         return Paragraph(
            OrderedListItemChunk,
            self._renderWikiText(para[2:])
         )
      else:
         return Paragraph(
            ParagraphChunk,
            self._renderWikiText(para)
         )


   def _isHeading(self, para):
      return _heading1RE.match(para)


   def _isUnorderedListItem(self, para):
      return para.startswith("* ")


   def _isOrderedListItem(self, para):
      return para.startswith("# ")


   def _headingChunk(self, para):
      numEqualSigns = 0
      for c in para:
         if c == "=":
            numEqualSigns += 1
         else:
            break

      if numEqualSigns > 5:
         numEqualSigns = 5

      return _headingChunks[numEqualSigns - 1]


   def _headingText(self, para):
      m = re.match(_parseHeading, para)
      return m.groupdict()["between"].strip()


   def _renderWikiText(self, para):
      return self._replacer.replaceWords(para)


class LineBreak:
   pass


class ParagraphList:

   def __init__(self):
      self._list = []
      self.inPara = False


   def startNewPara(self, newPara):
      self.inPara = True
      self._list.append(newPara)


   def appendToCurrentPara(self, text):
      if not self.inPara:
         self.startNewPara(text)
      else:
         self._list[-1] += " " + text


   def completePara(self, para):
      self._list.append(para)
      self.inPara = False


   def endPara(self):
      self.inPara = False


   def getList(self):
      return self._list


def _parseParas(lines):
   paras = ParagraphList()

   for line in lines:
      line = line.rstrip()
      if line:
         if line.startswith("="):
            paras.completePara(line)
         elif line.startswith("* "):
            paras.startNewPara(line)
         elif _isHorizontalRule(line):
            paras.completePara(line)
         elif line.startswith("# "):
            paras.startNewPara(line)
         elif _startsWithOneSpace(line) and paras.inPara:
            paras.completePara(LineBreak())
            paras.startNewPara(line[1:])
         else:
            paras.appendToCurrentPara(line)
      else:
         paras.endPara()
         
   return paras.getList()
      

def _isHorizontalRule(para):
   for c in para.rstrip():
      if c != "-":
         return False

   return True

      
def _startsWithOneSpace(line):
   try:
      assume(line[0] == " " and line[1] != " ")
   except (WikiTextException, IndexError):
      return False
   return True

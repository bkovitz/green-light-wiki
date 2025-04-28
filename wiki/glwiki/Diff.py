from difflib import SequenceMatcher
import re

insertRe = re.compile("^@@i\s*(\d+)$")
terminatorRe = re.compile("^@@$")
deleteOneLineRe = re.compile("^@@d\s*(\d+)$")
deleteMultipleLinesRe = re.compile("^@@d\s*(\d+)\s*,\s*(\d+)$")
replaceRe = re.compile("^@@r\s*(\d+)$")

matcher = SequenceMatcher(None)

ST_START = 0
ST_INSERT = 1
ST_REPLACE = 2

def makeDiff(before, after):
   result = []
   matcher.set_seqs(before, after)

   for tag, i1, i2, j1, j2 in matcher.get_opcodes():
      if tag == "insert":
         result.append("@@i%d" % (i1 + 1))
         result += after[j1:j2]
      elif tag == "delete":
         result.append(_makeDelete(i1, i2))
      elif tag == "replace":
         result.append(_makeDelete(i1, i2))
         result.append("@@i%d" % (i2 + 1))
         result += after[j1:j2]

   return result


def _makeDelete(i1, i2):
   if i1 + 1 == i2:
      return "@@d%d" % (i1 + 1)
   else:
      return "@@d%d,%d" % (i1 + 1, i2 - i1)



def reconstruct(before, diff):
   result = before[:]
   numInsertedLines = 0
   state = ST_START

   for originalLine in diff:
      line = originalLine.rstrip()

      match = insertRe.match(line)
      if match:
         insertionIndex = int(match.groups()[0]) + numInsertedLines - 1
         state = ST_INSERT
         continue

      match = terminatorRe.match(line)
      if match:
         state = ST_START
         continue

      match = deleteOneLineRe.match(line)
      if match:
         del result[int(match.groups()[0]) + numInsertedLines - 1]
         numInsertedLines -= 1
         state = ST_START
         continue

      match = deleteMultipleLinesRe.match(line)
      if match:
         startLine, numLines = match.groups()
         startLine = int(startLine) + numInsertedLines - 1
         numLines = int(numLines)
         del result[startLine : startLine + numLines]
         numInsertedLines -= numLines
         state = ST_START
         continue

      match = replaceRe.match(line)
      if match:
         replacementIndex = int(match.groups()[0]) + numInsertedLines - 1
         state = ST_REPLACE
         continue

      if state == ST_INSERT:
         result.insert(insertionIndex, originalLine)
         numInsertedLines += 1
         insertionIndex += 1
         continue

      if state == ST_REPLACE:
         if replacementIndex < len(result):
            result[replacementIndex] = originalLine
         else:
            result.append(originalLine)
         replacementIndex += 1
         continue
         

   return result

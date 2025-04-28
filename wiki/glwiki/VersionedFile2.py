import time, re
from difflib import SequenceMatcher

from Diff import makeDiff, reconstruct

versionRE = re.compile("^@@\s*version\s+")

class BadVersionException(Exception):

   def __init__(self, versionNum=None):
      self.versionNum = versionNum

   def __str__(self):
      return "non-existent wiki-page version: %s" % str(self.versionNum)


class Version:

   def __init__(self, versionInfo, lines):
      self.info = versionInfo
      self.lines = lines


class VersionInfo:

   def __init__(self, versionNum, dateString, author):
      self.versionNum = int(versionNum)
      self.date = dateString
      if not author.strip():
         author = "(unknown)"
      self.author = author


   def versionLine(self):
      return "@@ version %d; date %s; author %s;\n" % (
         int(self.versionNum),
         str(self.date),
         str(self.author)
      )


class VersionedFile2:

   def __init__(self, file_):
      self._file = file_
      self._versions = self._readAllVersions()
      self._reconstructFromDiffs()


   def writeNewVersion(self, author, lines):
      self._writeNewVersion(author, _dateString(), lines)


   def _writeNewVersion(self, author, dateString, lines):
      self._file.seek(0, 2)
      info = VersionInfo(self.getLatestVersionNum() + 1, dateString, author)
      self._file.write(info.versionLine())
      self._file.writelines(
         _addLineBreaksIfNeeded(self._diffLinesForNewVersion(lines))
      )
      self._file.flush()
      self._versions[info.versionNum] = Version(info, lines)


   def getLatestVersionNum(self):
      try:
         return max(self._versions.keys())
      except ValueError:
         return 0


   def getLatestVersion(self):
      latestVersionNum = self.getLatestVersionNum()
      if latestVersionNum == 0:
         return None
      else:
         return self.getVersion(latestVersionNum)


   def getLatestAuthor(self):
      latestVersionNum = self.getLatestVersionNum()
      if latestVersionNum == 0:
         return "(unknown)"
      else:
         return self.getVersionInfo(latestVersionNum).author


   def getVersionInfo(self, versionNum):
      try:
         return self._versions[versionNum].info
      except KeyError:
         raise BadVersionException(versionNum)


   def getVersion(self, versionNum):
      try:
         return self._versions[versionNum].lines
      except KeyError:
         raise BadVersionException(versionNum)


   def getPlusMinus(self, versionNum):
      if versionNum == 1:
         return len(self._versions[1].lines), 0

      plus = 0
      minus = 0

      matcher = SequenceMatcher(None)
      matcher.set_seqs(
         self._versions[versionNum - 1].lines,
         self._versions[versionNum].lines
      )

      for tag, i1, i2, j1, j2 in matcher.get_opcodes():
         if tag == "insert":
            plus += j2 - j1
         elif tag == "replace":
            plus += j2 - j1
            minus += i2 - i1
         elif tag == "delete":
            minus += i2 - i1

      return plus, minus


   def getPreviousAuthorsLastEdit(self, baselineVersionNum):
      lastAuthor = self.getVersionInfo(baselineVersionNum).author

      for versionNum in range(baselineVersionNum, 0, -1):
         if self.getVersionInfo(versionNum).author != lastAuthor:
            return self.getVersion(versionNum)

      return None


   def close(self):
      self._file.close()


   def _readAllVersions(self):
      result = {}
      try:
         self._file.seek(0)
      except AttributeError:
         return result

      for line in self._file.readlines():
         if versionRE.match(line):
            version = Version(_parseVersionLine(line), [])
            currentVersionLines = version.lines
            result[version.info.versionNum] = version
         else:
            if len(result) == 0:  # if this is the first line of a plain file
               info = VersionInfo(1, "0.0.0.0.0.0", "(unknown)")
               currentVersionLines = [line]
               result[1] = Version(info, currentVersionLines)
            else:
               currentVersionLines.append(line)

      return result


   def _diffLinesForNewVersion(self, lines):
      latestVersionNum = self.getLatestVersionNum()
      if latestVersionNum == 0:
         return lines
      else:
         return makeDiff(self.getVersion(latestVersionNum), lines)


   def _reconstructFromDiffs(self):
      #versionNumbers = self._versions.keys()
      versionNumbers = list(self._versions.keys())
      versionNumbers.sort()
      for index in range(len(versionNumbers)):
         if index > 0:  # don't treat 1st version as a diff
            thisVersion = self._versions[versionNumbers[index]]
            previousVersion = self._versions[versionNumbers[index - 1]]
            thisVersion.lines = \
               reconstruct(previousVersion.lines, thisVersion.lines)


def _addLineBreaksIfNeeded(lines):
   return [ _lineWithNewline(line) for line in lines ]


def _lineWithNewline(line):
   if line[-1] != "\n":
      return line + "\n"
   else:
      return line


def _dateString():
   return ".".join([ str(n) for n in time.gmtime()[:6] ])


def _parseVersionLine(line):
   result = {}

   if not line.startswith("@@"):
      return result

   line = line[2:].strip()

   for nameValuePair in re.split(";\s*", line):
      words = re.split("\s+", nameValuePair, 1)
      if len(words) == 2:
         result[words[0]] = words[1]

   return VersionInfo(result["version"], result["date"], result["author"])



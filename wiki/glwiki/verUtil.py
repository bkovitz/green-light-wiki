import sys, os, re

from VersionedFile import VersionedFile
from VersionedFile2 import VersionedFile2

def convertOneFile(filename):
   inputFile = file(filename, "r")
   outputFile = file("/tmp/ben", "w+")
   readAndWrite(inputFile, outputFile)
   inputFile.close()
   outputFile.close()
   escapedFilename = re.escape(filename)
   if os.system("rm %s" % escapedFilename) >> 8 != 0:
      sys.exit(1)
   if os.system("mv /tmp/ben %s" % escapedFilename) >> 8 != 0:
      sys.exit(1)


def readAndWrite(oldFile, newFile):
   v1 = VersionedFile(oldFile)
   v2 = VersionedFile2(newFile)

   for versionNum in range(1, v1.getLatestVersionNum() + 1):
      v1info = v1.getVersionInfo(versionNum)
      v1text = v1.getVersion(versionNum)

      v2._writeNewVersion(v1info.author, v1info.date, v1text)


for filename in sys.argv[1:]:
   if os.path.isfile(filename):
      print filename
      convertOneFile(filename)

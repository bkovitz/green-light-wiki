from teest import *
from StringIO import StringIO

from VersionedFile import VersionedFile, VersionInfo, _parse, \
   BadVersionException
from WikiCommand import WikiCommand

class ut_VersionedFile:

   def testOneEntry(self):
      fakeFile = StringIO(
"""@@ version 1; date 2003.07.24.04.50.57; author BenKovitz;
@@ hereis 1
This is a line of text.
""")

      v = VersionedFile(fakeFile)

      TEST_EQ(1, v.numVersions())
      TEST_EQ(["This is a line of text.\n"], v.getVersion(1))


   def testTwoEntries(self):
      fakeFile = StringIO(
"""@@ version 2; date 2003.07.24.04.50.57; author BenKovitz;
@@ version 1; date 2003.05.19.01.00.42; author BenKovitz;
@@ hereis 2
This version is different than the previous one.
It contains two lines.
@@ hereis 1
This is a line of text.
""")

      v = VersionedFile(fakeFile)

      TEST_EQ(2, v.numVersions())
      TEST_EQ(
         ["This is a line of text.\n"],
         v.getVersion(1)
      )
      TEST_EQ(
         [
            "This version is different than the previous one.\n",
            "It contains two lines.\n",
         ],
         v.getVersion(2)
      )


   def testGetNonexistentVersion(self):
      fakeFile = StringIO(
"""@@ version 2; date 2003.07.24.04.50.57; author BenKovitz;
@@ version 1; date 2003.05.19.01.00.42; author BenKovitz;
@@ hereis 2
This version is different than the previous one.
It contains two lines.
@@ hereis 1
This is a line of text.
""")

      v = VersionedFile(fakeFile)
      TEST_EXC(BadVersionException, v.getVersion, 3)


   def testGetLatestVersion(self):
      fakeFile = StringIO(
"""@@ version 2; date 2003.07.24.04.50.57; author BenKovitz;
@@ version 1; date 2003.05.19.01.00.42; author BenKovitz;
@@ hereis 2
This version is different than the previous one.
It contains two lines.
@@ hereis 1
This is a line of text.
""")

      v = VersionedFile(fakeFile)

      TEST_EQ(
         [
            "This version is different than the previous one.\n",
            "It contains two lines.\n",
         ],
         v.getLatestVersion()
      )


   def testWriteNewFile(self):
      fakeFile = StringIO()

      v = VersionedFile(fakeFile)

      lines = [
         "First line of the file\n",
         "Second line of the file\n",
      ]

      command = WikiCommand(
         "SAVE",
         "wikiname-ignored",
         "pagename-ignored",
         StringIO("".join(lines)),
         "BenKovitz"
      )

      v.writeNewVersion(command)

      expect = \
"""@@ version 1; date [0-9.]+; author BenKovitz;
@@ hereis 1
First line of the file
Second line of the file
"""
      TEST(re.match(expect, fakeFile.getvalue()))


   def testWriteNewVersion(self):
      fakeFile = StringIO(
"""@@ version 1; date 12.34.56.78.12.34; author BenKovitz;
@@ hereis 1
First line of the file
Second line of the file
""")
      v = VersionedFile(fakeFile)

      newVersion = "This is a revised version with no newline."

      command = WikiCommand(
         "SAVE",
         "wikiname-ignored",
         "pagename-ignored",
         StringIO(newVersion),
         "GeorgeGibbons"
      )

      v.writeNewVersion(command)

      expect = \
"""@@ version 2; date [0-9.]+; author GeorgeGibbons;
@@ version 1; date 12.34.56.78.12.34; author BenKovitz;
@@ hereis 2
This is a revised version with no newline.
@@ hereis 1
First line of the file
Second line of the file
"""
      TEST(re.match(expect, fakeFile.getvalue()))


   def testGetVersionList(self):
      fakeFile = StringIO(
"""@@ version 2; date [0-9].+; author GeorgeGibbons;
@@ version 1; date [0-9.]+; author BenKovitz;
@@ hereis 2
This is a revised version.
@@ hereis 1
First line of the file
Second line of the file
""")

      v = VersionedFile(fakeFile)

      versionList = v.getVersionList()

      TEST_EQ(2, len(versionList))
      TEST_EQ(2, int(versionList[0].version))
      TEST_EQ("GeorgeGibbons", versionList[0].author)
      TEST_EQ(1, int(versionList[1].version))
      TEST_EQ("BenKovitz", versionList[1].author)


   def testGetVersionInfo(self):
      fakeFile = StringIO(
"""@@ version 2; date 12.34.56.78.12.34; author GeorgeGibbons;
@@ version 1; date 12.34.56.78.12.35; author BenKovitz;
@@ hereis 2
This is a revised version.
@@ hereis 1
First line of the file
Second line of the file
""")

      v = VersionedFile(fakeFile)

      got = v.getVersionInfo(1)
      TEST_EQ("1", got.version)
      TEST_EQ("12.34.56.78.12.35", got.date)
      TEST_EQ("BenKovitz", got.author)

      got = v.getVersionInfo(2)
      TEST_EQ("2", got.version)
      TEST_EQ("12.34.56.78.12.34", got.date)
      TEST_EQ("GeorgeGibbons", got.author)

      
   def testgetLatestVersionNum(self):
      fakeFile = StringIO(
"""@@ version 2; date 12.34.56.78.12.34; author GeorgeGibbons;
@@ version 1; date 12.34.56.78.12.35; author BenKovitz;
@@ hereis 2
This is a revised version.
@@ hereis 1
First line of the file
Second line of the file
""")
      v = VersionedFile(fakeFile)

      TEST_EQ(2, v.getLatestVersionNum())


   def testLineParser(self):
      line = "@@ version 2; date 12.34.56.78.12.34; author JohnQMittens;"
      
      d = _parse(line)

      TEST_EQ("2", d["version"])
      TEST_EQ("12.34.56.78.12.34", d["date"])
      TEST_EQ("JohnQMittens", d["author"])


   def testMaxVersionNum1(self):
      fakeFile = StringIO(
"""@@ version 1; date 12.34.56.78.12.34; author BenKovitz;
@@ hereis 1
First line of the file
Second line of the file
""")
      v = VersionedFile(fakeFile)

      TEST_EQ(1, v.maxVersionNum())


   def testMaxVersionNum2(self):
      fakeFile = StringIO(
"""@@ version 2; date [0-9].+; author GeorgeGibbons;
@@ version 1; date [0-9.]+; author BenKovitz;
@@ hereis 2
This is a revised version.
@@ hereis 1
First line of the file
Second line of the file
""")

      v = VersionedFile(fakeFile)

      TEST_EQ(2, v.maxVersionNum())


   def testMaxVersionNum1NonVersioned(self):
      fakeFile = StringIO(
"""No versioning in this file.

Third line.
""")
      v = VersionedFile(fakeFile)

      TEST_EQ(1, v.maxVersionNum())


   def testMaxVersionNum0(self):
      fakeFile = StringIO()
      v = VersionedFile(fakeFile)

      TEST_EQ(0, v.maxVersionNum())


   def teestReadNonVersionedFile(self):
      fakeFile = StringIO(
"""No versioning in this file.

Third line.
""")
      v = VersionedFile(fakeFile)

      expect = [
         "No versioning in this file.\n",
         "\n",
         "Third line.\n"
      ]

      TEST_EQ(expect, v.getLatestVersion())
      
      vlist = v.getVersionList()

      TEST_EQ(1, len(vlist))
      TEST_EQ(1, int(vlist[0].version))
      TEST_EQ("(unknown)", vlist[0].author)

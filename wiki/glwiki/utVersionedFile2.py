from teest import *

from VersionedFile2 import VersionedFile2

from StringIO import StringIO
import re

dateStringRE = \
   re.compile("\d\d\d\d\.\d{1,2}\.\d{1,2}\.\d{1,2}\.\d{1,2}\.\d{1,2}")


class ut_VersionedFile2:

   def testWrite1Read1(self):
      f = StringIO()

      v = VersionedFile2(f)
      v.writeNewVersion("George Gibbons", ["first line\n", "second line\n"])
      TEST_EQ(1, v.getLatestVersionNum())

      v = VersionedFile2(f)
      TEST_EQ(1, v.getLatestVersionNum())
      expect = ["first line\n", "second line\n"]
      TEST_EQ(expect, v.getLatestVersion())

      info = v.getVersionInfo(1)
      TEST_EQ(1, info.versionNum)
      TEST(dateStringRE.match(info.date))
      TEST_EQ("George Gibbons", info.author)


   def testWrite2Read2(self):
      f = StringIO()

      v = VersionedFile2(f)
      v.writeNewVersion("George Gibbons", ["first line\n", "second line\n"])

      v = VersionedFile2(f)
      v.writeNewVersion("Dr. John Mittens",
         ["first line\n", "second line\n", "third line\n"]
      )

      v = VersionedFile2(f)
      TEST_EQ(2, v.getLatestVersionNum())
      expect = ["first line\n", "second line\n", "third line\n"]
      TEST_EQ(expect, v.getLatestVersion())

      info = v.getVersionInfo(2)
      TEST_EQ(2, info.versionNum)
      TEST(dateStringRE.match(info.date))
      TEST_EQ("Dr. John Mittens", info.author)
      expect = ["first line\n", "second line\n", "third line\n"]
      TEST_EQ(expect, v.getVersion(2))

      info = v.getVersionInfo(1)
      TEST_EQ(1, info.versionNum)
      TEST(dateStringRE.match(info.date))
      TEST_EQ("George Gibbons", info.author)
      expect = ["first line\n", "second line\n"]
      TEST_EQ(expect, v.getVersion(1))


   def testReadPlainFile(self):
      f = StringIO("First line\nSecond line\n")

      v = VersionedFile2(f)
      TEST_EQ(1, v.getLatestVersionNum())
      expect = ["First line\n", "Second line\n"]
      TEST_EQ(expect, v.getLatestVersion())

      info = v.getVersionInfo(1)
      TEST_EQ(1, info.versionNum)
      TEST_EQ("0.0.0.0.0.0", info.date)
      TEST_EQ("(unknown)", info.author)


   def testGetPreviousAuthorsLastEdit(self):
      f = StringIO()

      v = VersionedFile2(f)
      v.writeNewVersion("George Gibbons",
         ["george one\n", "george three\n"]
      )
      v.writeNewVersion("George Gibbons",
         ["george one\n", "george two\n", "george three\n"]
      )
      v.writeNewVersion("Dr. John Mittens",
         ["george one\n", "john one\n", "george three\n"]
      )
      v.writeNewVersion("Dr. John Mittens",
         ["george one\n", "john one\n", "george three\n", "john two\n"]
      )
      v.writeNewVersion("George Gibbons",
         ["john one\n", "george three\n", "john two\n"]
      )

      v = VersionedFile2(f)

      expect = ["george one\n", "george two\n", "george three\n"]
      TEST_EQ(expect, v.getPreviousAuthorsLastEdit(4))

      expect = ["george one\n", "john one\n", "george three\n", "john two\n"]
      TEST_EQ(expect, v.getPreviousAuthorsLastEdit(5))


   def testNoPreviousAuthor(self):
      f = StringIO()

      v = VersionedFile2(f)
      v.writeNewVersion("George Gibbons",
         ["george one\n", "george three\n"]
      )
      v.writeNewVersion("George Gibbons",
         ["george one\n", "george two\n", "george three\n"]
      )

      v = VersionedFile2(f)
      TEST_EQ(None, v.getPreviousAuthorsLastEdit(2))


   def testPlusMinus(self):
      f = StringIO()

      v = VersionedFile2(f)
      v.writeNewVersion("George Gibbons",
         ["george one\n", "george three\n"]
      )
      v.writeNewVersion("George Gibbons",
         ["george one\n", "george two\n", "george three\n"]
      )
      v.writeNewVersion("Dr. John Mittens",
         ["george one\n", "john one\n", "george three\n"]
      )
      v.writeNewVersion("Dr. John Mittens",
         ["george one\n", "john one\n", "george three\n", "john two\n"]
      )
      v.writeNewVersion("George Gibbons",
         ["john one\n", "george three\n", "john two\n"]
      )

      v = VersionedFile2(f)

      TEST_EQ((2, 0), v.getPlusMinus(1))  # 2 lines added, none lost
      TEST_EQ((1, 0), v.getPlusMinus(2))
      TEST_EQ((1, 1), v.getPlusMinus(3))
      TEST_EQ((1, 0), v.getPlusMinus(4))
      TEST_EQ((0, 1), v.getPlusMinus(5))


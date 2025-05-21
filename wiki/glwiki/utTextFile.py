from teest import *
from utMisc import forceRemove

from TextFile import TextFile


testFileName = "TESTDATA/textfile"


class ut_TextFile:

    def setUp(self):
        forceRemove(testFileName)

    def tearDown(self):
        forceRemove(testFileName)

    def testLinesFromNonexistentFile(self):
        f = TextFile(testFileName)
        TEST_EQ([], f.lines())

    def testLinesFromRealFile(self):
        f = open(testFileName, "w")
        f.write("first line\nsecond line\n")
        del f

        f = TextFile(testFileName)
        TEST_EQ(["first line", "second line"], f.lines())

    def testStrFromNonexistentFile(self):
        TEST_EQ("", str(TextFile(testFileName)))

    def testStrFromRealFile(self):
        f = open(testFileName, "w")
        f.write("first line\nsecond line\n")
        del f

        TEST_EQ("first line\nsecond line\n", str(TextFile(testFileName)))

    def testWriteNewFile(self):
        TextFile(testFileName).write("some text\nsome more text\n")

        realFile = open(testFileName, "r")
        TEST_EQ("some text\nsome more text\n", realFile.read())

    def testReadOneLineAtATime(self):
        TextFile(testFileName).write("a line\nanother line\nstill another\n")

        f = TextFile(testFileName)
        TEST_EQ("a line", f[0])
        TEST_EQ("another line", f[1])
        TEST_EQ("still another", f[2])

    def testReadPastEndOfFile(self):
        TextFile(testFileName).write("a line\nanother line\nstill another\n")
        TEST_EQ("", TextFile(testFileName)[3])

    def testModifyLines(self):
        TextFile(testFileName).write("a line\nanother line\nstill another\n")

        f = TextFile(testFileName)
        f[1] = "brand new line"
        del f

        TEST_EQ("a line\nbrand new line\nstill another\n", TextFile(testFileName))

    def testModifyAndThenRead(self):
        f = TextFile(testFileName)
        f[0] = "zero"
        f[1] = "one"
        f[2] = "two"

        TEST_EQ(f[0], "zero")
        TEST_EQ("zero\none\ntwo\n", f)

        del f

        TEST_EQ("zero\none\ntwo\n", TextFile(testFileName))

    def testIterator(self):
        TextFile(testFileName).write("a line\nanother line\nstill another\n")

        lines = [line for line in TextFile(testFileName)]
        expect = ["a line", "another line", "still another"]
        TEST_EQ(expect, lines)

    def testWriteList(self):
        TextFile(testFileName).write(["unum", "duo", "tria"])

        TEST_EQ("unum\nduo\ntria\n", TextFile(testFileName))

    def testEq(self):
        TextFile(testFileName).write("some\ntext\n")

        TEST("some\ntext\n" == TextFile(testFileName))
        TEST(not "some\ntext\n" != TextFile(testFileName))
        TEST(not "other\ntext\n" == TextFile(testFileName))
        TEST("other\ntext\n" != TextFile(testFileName))
        TEST(TextFile(testFileName) == "some\ntext\n")
        TEST(not TextFile(testFileName) != "some\ntext\n")
        TEST(not TextFile(testFileName) == "other\ntext\n")
        TEST(TextFile(testFileName) != "other\ntext\n")

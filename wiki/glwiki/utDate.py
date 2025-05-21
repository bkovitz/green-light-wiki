from teest import *

from Date import Date


class ut_Date:

    def testLongInputFormat(self):
        d = Date("August 15, 2003")

        TEST_EQ("August 15, 2003", str(d))

    def testMediumInputFormat(self):
        d = Date("Aug 15, 2003")

        TEST_EQ("August 15, 2003", str(d))

    def testShortButClearInputFormat(self):
        d = Date("15-Aug-2003")

        TEST_EQ("August 15, 2003", str(d))

    def testAddition(self):
        d = Date("Sept 9, 2003")

        TEST_EQ("September 23, 2003", str(d + 14))

    def testSubtraction(self):
        d = Date("23-Sep-2003")

        TEST_EQ("September 9, 2003", str(d - 14))

    def testEquality(self):
        d1 = Date("25-Sep-2003")
        d2 = Date("September 25, 2003")
        d3 = Date("26-Sep-2003")

        TEST(d1 == d1)
        TEST(d1 == d2)
        TEST(d2 == d1)
        TEST(d1 != d3)
        TEST(d3 != d1)

    def testComparison(self):
        d1 = Date("25-Sep-2003")
        d2 = Date("September 25, 2003")
        d3 = Date("26-Sep-2003")
        d4 = Date("Sep 24, 2003")

        TEST_EQ(0, cmp(d1, d2))
        TEST_EQ(0, cmp(d1, d1))
        TEST(cmp(d1, d3) < 0)
        TEST(cmp(d1, d4) > 0)

    def testDefaultTo2000(self):
        d = Date("25-Sep-03")

        TEST_EQ("September 25, 2003", str(d))

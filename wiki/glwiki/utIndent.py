from teest import *
import os

from Indent import Indent

class ut_Indent:

    def testIndent(self):
        indent = Indent()

        TEST_EQ(str(indent), "")  # level 0

        indent.increment()

        TEST_EQ(str(indent), "  ")  # level 1

        indent.increment()

        TEST_EQ(str(indent), "    ")  # level 2

        indent.decrement()

        TEST_EQ(str(indent), "  ")  # level 1

        indent.decrement()

        TEST_EQ(str(indent), "")  # level 0

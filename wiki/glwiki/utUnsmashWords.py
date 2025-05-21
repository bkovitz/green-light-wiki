from teest import *

from UnsmashWords import unsmashWords


class ut_UnsmashWords:

    def testUnsmashWords(self):
        TEST_EQ("One Two", unsmashWords("OneTwo"))
        TEST_EQ("One Two", unsmashWords("One_Two"))
        TEST_EQ("One about Two", unsmashWords("One_about_Two"))
        TEST_EQ("Lev 1 lev 2", unsmashWords("Lev_1_lev_2"))
        TEST_EQ("OneTwo", unsmashWords("OneTwo_"))
        TEST_EQ("djkfhdjsfhjkdhf", unsmashWords("djkfhdjsfhjkdhf"))
        TEST_EQ("What is this wiki?", unsmashWords("What_is_this_wiki?"))

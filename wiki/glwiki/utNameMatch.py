from teest import *

from NameMatch import bestName


class ut_NameMatch:

    def testAll(self):
        names = ["Blah", "HackathonNotes"]

        TEST_EQ("HackathonNotes", bestName(names, "Hackathon_Notes"))

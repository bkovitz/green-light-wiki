from teest import *
from Misc import forceRemove

from Log import log


class ut_Log:

    def testLog(self):
        fakeEnvironment = {
            "REMOTE_ADDR": "100.101.102.103",
            "HTTP_REFERER": "http://yahoo.com",
        }

        forceRemove("wikilog")
        log(fakeEnvironment, "DISP", "/heuristic/WelcomePage", "Unknown_User")

        logFile = open("wikilog", "r")
        logData = logFile.readlines()

        TEST_EQ(1, len(logData))

        words = logData[0].split()

        TEST_EQ(7, len(words))
        TEST_EQ("Unknown_User(100.101.102.103)", words[3])
        TEST_EQ("DISP", words[4])
        TEST_EQ("heuristic/WelcomePage", words[5])
        TEST_EQ("http://yahoo.com", words[6])

        del logFile

    def testBlanksIntoHyphens(self):
        fakeEnvironment = {
            "REMOTE_ADDR": "100.101.102.103",
            # no HTTP_REFERER
        }

        forceRemove("wikilog")
        log(fakeEnvironment, "DISP", "", "")

        logFile = open("wikilog", "r")
        logData = logFile.readlines()

        TEST_EQ(1, len(logData))

        words = logData[0].split()

        TEST_EQ(7, len(words))
        TEST_EQ("100.101.102.103", words[3])
        TEST_EQ("DISP", words[4])
        TEST_EQ("-", words[5])
        TEST_EQ("-", words[6])

        del logFile

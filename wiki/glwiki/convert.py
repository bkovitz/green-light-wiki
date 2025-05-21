import sys, os, operator, re
from io import StringIO

START = 0
GOT_BRACKET = 1
GOT_FIRST_UPPER = 2
IN_WIKIWORD = 3
IN_ODD_WORD = 4


class Transition:

    def __init__(self, tokenTest, actionMethod, nextState):
        self.tokenTest = tokenTest
        self.actionMethod = actionMethod
        self.nextState = nextState


class StateMachine:

    def __init__(self, outputFile):
        self.outputFile = outputFile
        self.state = START
        self.word = ""

        self.stateTransitions = {
            START: [
                Transition(lambda c: c == "[", self.clearWord, GOT_BRACKET),
                Transition(lambda c: c.isupper(), self.setWord, GOT_FIRST_UPPER),
                Transition(lambda c: True, self.dumpChar, START),
            ],
            GOT_BRACKET: [
                Transition(lambda c: c == "]", self.linkWord, START),
                Transition(lambda c: c == "\n", self.dumpWordAndChar, START),
                Transition(lambda c: True, self.appendChar, GOT_BRACKET),
            ],
            GOT_FIRST_UPPER: [
                Transition(lambda c: c.isupper(), self.dumpWordAndChar, IN_ODD_WORD),
                Transition(lambda c: c.islower(), self.appendChar, IN_WIKIWORD),
                Transition(lambda c: True, self.dumpWordAndChar, START),
            ],
            IN_WIKIWORD: [
                Transition(lambda c: c.isupper(), self.appendChar, IN_WIKIWORD),
                Transition(lambda c: c.islower(), self.appendChar, IN_WIKIWORD),
                Transition(lambda c: True, self.dumpWikiWordChar, START),
            ],
            IN_ODD_WORD: [
                Transition(lambda c: c.isalnum(), self.dumpChar, IN_ODD_WORD),
                Transition(lambda c: True, self.dumpChar, START),
            ],
        }

    def feedChar(self, c):
        transitionList = self.stateTransitions[self.state]
        for transition in transitionList:
            if transition.tokenTest(c):
                transition.actionMethod(c)
                self.state = transition.nextState
                return

        assert "should never get here"

    def clearWord(self, c):
        self.word = ""

    def setWord(self, c):
        self.word = c

    def linkWord(self, c):
        self.outputFile.write("[[" + self.word + "]]")

    def dumpWordAndChar(self, c):
        self.outputFile.write(self.word + c)

    def appendChar(self, c):
        self.word += c

    def dumpWikiWordChar(self, c):
        if self.numberOfCapitals() >= 2:
            self.addSpacesBeforeCapitals()
            self.linkWord(c)
        else:
            self.dumpWord()
        self.dumpChar(c)

    def dumpWord(self):
        self.outputFile.write(self.word)

    def dumpChar(self, c):
        self.outputFile.write(c)

    def numberOfCapitals(self):
        return reduce(operator.add, [c.isupper() for c in self.word])

    def addSpacesBeforeCapitals(self):
        newWord = self.word[0]
        for c in self.word[1:]:
            if c.isupper():
                newWord += " "
            newWord += c

        self.word = newWord


def readAndWrite(oldFile, newFile):
    stateMachine = StateMachine(newFile)
    for line in oldFile:
        if line.startswith("@@"):
            newFile.write(line)
        else:
            for c in line:
                stateMachine.feedChar(c)


def convertOneFile(filename):
    inputFile = open(filename, "r")
    outputFile = open("/tmp/ben", "w")
    readAndWrite(inputFile, outputFile)
    inputFile.close()
    outputFile.close()
    escapedFilename = re.escape(filename)
    if os.system("rm %s" % escapedFilename) >> 8 != 0:
        sys.exit(1)
    if os.system("mv /tmp/ben %s" % escapedFilename) >> 8 != 0:
        sys.exit(1)


def convertAllFilesInThisDirectory():
    for filename in os.listdir("."):
        if os.path.isfile(filename):
            print(filename)
            convertOneFile(filename)


readAndWrite(StringIO("text\n"), sys.stdout)
readAndWrite(StringIO("Text words\n"), sys.stdout)
readAndWrite(StringIO("text [A Link] more text\n"), sys.stdout)
readAndWrite(StringIO("text [Not A Link\n"), sys.stdout)
readAndWrite(StringIO("text WikiWord more text\n"), sys.stdout)
readAndWrite(StringIO("text ODDWord more text\n"), sys.stdout)
readAndWrite(StringIO("text WikiWord\n"), sys.stdout)
readAndWrite(StringIO("@@hereis 1\ntext WikiWord\n"), sys.stdout)

"""
convertAllFilesInThisDirectory()
"""

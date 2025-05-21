from teest import *

from Diff import makeDiff, reconstruct


class ut_Diff:

    def testInsertInMiddle(self):
        a1 = ["first", "second", "third"]
        a2 = ["first", "second", "after second", "third"]

        expect = "@@i3\nafter second\n".splitlines()

        TEST_EQ(expect, makeDiff(a1, a2))

    def testInsertAtBeginning(self):
        a1 = ["second", "third"]
        a2 = ["first", "second", "third"]

        expect = "@@i1\nfirst\n".splitlines()

        TEST_EQ(expect, makeDiff(a1, a2))

    def testAppend(self):
        a1 = ["first", "second", "third"]
        a2 = ["first", "second", "third", "fourth"]

        expect = "@@i4\nfourth\n".splitlines()

        TEST_EQ(expect, makeDiff(a1, a2))

    def testTwoInsertions(self):
        a1 = ["first", "second", "third"]
        a2 = ["first", "second", "after second", "third", "after third"]

        expect = "@@i3\nafter second\n@@i4\nafter third\n".splitlines()

        TEST_EQ(expect, makeDiff(a1, a2))

    def testDeleteOneLine(self):
        a1 = ["first", "second", "third", "fourth"]
        a2 = ["first", "second", "third"]

        expect = ["@@d4"]

        TEST_EQ(expect, makeDiff(a1, a2))

    def testDeleteTwoLines(self):
        a1 = ["first", "second", "third", "fourth"]
        a2 = ["first", "fourth"]

        expect = ["@@d2,2"]

        TEST_EQ(expect, makeDiff(a1, a2))

    def testInsertionAndDeletion(self):
        a1 = ["first", "second", "third"]
        a2 = ["zeroth", "first", "third"]

        expect = "@@i1\nzeroth\n@@d2\n".splitlines()

        TEST_EQ(expect, makeDiff(a1, a2))

    def testReplaceOneLine(self):
        a1 = ["first", "second", "third"]
        a2 = ["first", "new", "third"]

        diff = makeDiff(a1, a2)
        TEST_EQ(a2, reconstruct(a1, diff))

    def testReconstructOneLineInsertion(self):
        a1 = ["first", "second", "third"]
        diff = "@@i3\nafter second\n@@\n".splitlines()

        expect = ["first", "second", "after second", "third"]

        TEST_EQ(expect, reconstruct(a1, diff))

    def testReconstructMultilineInsertion(self):
        a1 = ["first", "second", "third"]
        diff = "@@i3\nafter second\nalso after 2nd\n@@\n".splitlines()

        expect = ["first", "second", "after second", "also after 2nd", "third"]

        TEST_EQ(expect, reconstruct(a1, diff))

    def testReconstructOneLineDeletion(self):
        a1 = ["first", "second", "third", "fourth"]
        diff = ["@@d4"]

        expect = ["first", "second", "third"]

        TEST_EQ(expect, reconstruct(a1, diff))

    def testReconstructMultilineDeletion(self):
        a1 = ["first", "second", "third", "fourth"]
        diff = ["@@d2,2"]

        expect = ["first", "fourth"]

        TEST_EQ(expect, reconstruct(a1, diff))

    def testReconstructInsertionAndDeletion(self):
        a1 = ["first", "second", "third"]
        diff = "@@i1\nzeroth\n@@d2\n".splitlines()

        expect = ["zeroth", "first", "third"]

        TEST_EQ(expect, reconstruct(a1, diff))

    # TODO: get rid of @@r, it's now obsolete
    def testReconstructDeletionAndReplacement(self):
        a1 = ["first", "second", "third"]
        diff = "@@d1\n@@r2\nnew\n".splitlines()

        expect = ["new", "third"]

        TEST_EQ(expect, reconstruct(a1, diff))

    def testReconstructMultilineReplacement(self):
        a1 = ["first", "second", "third"]
        diff = "@@r1\nnew1\nnew2\nnew3\n".splitlines()

        expect = ["new1", "new2", "new3"]

        TEST_EQ(expect, reconstruct(a1, diff))

    def testReplaceDecreasesLines(self):
        a1 = [
            "This is just a test wiki for trying out new versions of the [[Green Light Wiki http://greenlightwiki.com]] software.\n",
            "\n",
            "----\n",
            "'''Gibberish begins here...'''\n",
            "\n",
        ]
        a2 = [
            "This is just a test wiki for trying out new versions of the [[Green Light Wiki http://greenlightwiki.com]] software.\n",
            "\n",
            "== Gibberish begins here... ==\n",
            "\n",
        ]

        diff = makeDiff(a1, a2)
        TEST_EQ(a2, reconstruct(a1, diff))

    def testReplaceIncreasesLines(self):
        a1 = ["first", "replaceme", "last"]
        a2 = ["first", "new1", "new2", "new3", "last"]

        diff = makeDiff(a1, a2)
        TEST_EQ(a2, reconstruct(a1, diff))

    # TODO: fail gracefully from invalid diff string

from teest import *
from utMisc import resetConfig

from LatexImage import LatexImage, LatexDatabase, clearLatexImages
from WikiRepository import WikiRepository
from ShellCommand import ShellCommand

gsCheck = ShellCommand("gs")
gsCheck.run()
gsIsInstalled = gsCheck.getResult() != 127


class ut_LatexImage:

    def setUp(self):
        clearLatexImages()
        resetConfig()

    def tearDown(self):
        clearLatexImages()

    def testLatexImage(self):
        if not gsIsInstalled:
            return

        image = LatexImage(WikiRepository("TESTWIKI"), "$\int_a^b e^{it}f(t)\,dt$")
        expect = (
            '<IMG CLASS="latex-image" SRC="http://greenlightwiki.com/latex000.jpg">'
        )
        TEST_EQ(expect, str(image))

    def testCachedImage(self):
        if not gsIsInstalled:
            return

        image = LatexImage(WikiRepository("TESTWIKI"), "$\int_a^b e^{it}f(t)\,dt$")
        str(image)

        image2 = LatexImage(WikiRepository("TESTWIKI"), "$\int_a^b e^{it}f(t)\,dt$")
        expect = (
            '<IMG CLASS="latex-image" SRC="http://greenlightwiki.com/latex000.jpg">'
        )
        TEST_EQ(expect, str(image2))

    def testFirstFilename(self):
        if not gsIsInstalled:
            return

        database = LatexDatabase()
        string = "$a$"
        TEST_EQ((1, "latex000.jpg"), database.getImageFilename(string))

    def testTwoFilenames(self):
        if not gsIsInstalled:
            return

        database = LatexDatabase()
        TEST_EQ((1, "latex000.jpg"), database.getImageFilename("$a$"))
        database.imageFileCreated("$a$")
        TEST_EQ((1, "latex001.jpg"), database.getImageFilename("$b$"))
        database.imageFileCreated("$b$")
        TEST_EQ((0, "latex000.jpg"), database.getImageFilename("$a$"))

    def testFilenameRollover(self):
        database = LatexDatabase()
        for i in range(1000):
            database.imageFileCreated("$" + "a" * (i + 1) + "$")

        TEST_EQ((0, "latex000.jpg"), database.getImageFilename("$a$"))
        TEST_EQ((1, "latex000.jpg"), database.getImageFilename("$b$"))

    def testDontBumpNextKeyIfCommandFailed(self):
        image = LatexImage(WikiRepository("TESTWIKI"), "$ignored$")
        image._makeCommands = lambda self: [ShellCommand("non-existent-command")]

        assert image._getDatabase()._getNextId() == 0

        TEST(str(image).startswith("&lt;&lt;LaTeX failure"))

        TEST_EQ(0, image._getDatabase()._getNextId())

    def testInsecureCommand(self):
        image = LatexImage(WikiRepository("TESTWIKI"), "$\\input$")
        TEST(str(image).startswith("&lt;&lt;&lt;Sorry"))

    def testInsecureCommandWithSpaces(self):
        image = LatexImage(WikiRepository("TESTWIKI"), "$\\begin { filecontents } $")
        TEST(str(image).startswith("&lt;&lt;&lt;Sorry"))

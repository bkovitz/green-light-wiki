from teest import *
from io import StringIO

from PathMatch import PathMatch, _convertToRegexp
from utMisc import NonexistentFile, FileFromList
from File import File


class ut_PathMatch:

    def testNoPathConfig(self):
        matcher = PathMatch(NonexistentFile("wiki.dirs"))

        wikiName, fileType, pageName = matcher.pathInfo("/somefile")
        TEST_EQ("", wikiName)
        TEST_EQ("WIKI", fileType)
        TEST_EQ("somefile", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/somefile.html")
        TEST_EQ("", wikiName)
        TEST_EQ("WIKI", fileType)
        TEST_EQ("somefile.html", pageName)

    def testSlashWithNoConfig(self):
        matcher = PathMatch(NonexistentFile("wiki.dirs"))

        wikiName, fileType, pageName = matcher.pathInfo("/somedir/somefile.html")
        TEST_EQ("", wikiName)
        TEST_EQ("BAD", fileType)
        TEST_EQ("somedir/somefile.html", pageName)

    def testStatic(self):
        paths = FileFromList(["STATIC *.html\n"])

        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("/somefile")
        TEST_EQ("", wikiName)
        TEST_EQ("BAD", fileType)
        TEST_EQ("somefile", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/somefile.html")
        TEST_EQ("", wikiName)
        TEST_EQ("STATIC", fileType)
        TEST_EQ("somefile.html", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/somedir/somefile.html")
        TEST_EQ("", wikiName)
        TEST_EQ("BAD", fileType)
        TEST_EQ("somedir/somefile.html", pageName)

    def testStaticInSubdirectory(self):
        paths = FileFromList(["STATIC statics/*.html\n"])

        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("/somefile")
        TEST_EQ("", wikiName)
        TEST_EQ("BAD", fileType)
        TEST_EQ("somefile", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/somefile.html")
        TEST_EQ("", wikiName)
        TEST_EQ("BAD", fileType)
        TEST_EQ("somefile.html", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/statics/somefile.html")
        TEST_EQ("", wikiName)
        TEST_EQ("STATIC", fileType)
        TEST_EQ("statics/somefile.html", pageName)

    def testMixture(self):
        paths = FileFromList(
            [
                "WIKI wiki/*",
                "WIKI *",
                "PLAIN plains/*.html\n",
                "STATIC statics/*.html\n",
            ]
        )

        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("/statics/somefile.html")
        TEST_EQ("", wikiName)
        TEST_EQ("STATIC", fileType)
        TEST_EQ("statics/somefile.html", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/plains/somefile.html")
        TEST_EQ("", wikiName)
        TEST_EQ("PLAIN", fileType)
        TEST_EQ("plains/somefile.html", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/wiki/SomePage")
        TEST_EQ("wiki", wikiName)
        TEST_EQ("WIKI", fileType)
        TEST_EQ("wiki/SomePage", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/TopPage")
        TEST_EQ("", wikiName)
        TEST_EQ("WIKI", fileType)
        TEST_EQ("TopPage", pageName)

    def testNamedWikis(self):
        paths = FileFromList(
            [
                "WIKI this-wiki wiki/*",
                "WIKI that-wiki that/*",
            ]
        )

        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("/wiki/PageName")
        TEST_EQ("this-wiki", wikiName)
        TEST_EQ("WIKI", fileType)
        TEST_EQ("wiki/PageName", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/that/OtherPage")
        TEST_EQ("that-wiki", wikiName)
        TEST_EQ("WIKI", fileType)
        TEST_EQ("that/OtherPage", pageName)

    def testDefaultWikiPageWithoutSlash(self):
        paths = FileFromList(
            [
                "WIKI this-wiki wiki/*",
                "WIKI that-wiki that/*",
            ]
        )

        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("/wiki")
        TEST_EQ("WIKI", fileType)
        TEST_EQ("this-wiki", wikiName)
        TEST_EQ("wiki/WelcomePage", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/that")
        TEST_EQ("WIKI", fileType)
        TEST_EQ("that-wiki", wikiName)
        TEST_EQ("that/WelcomePage", pageName)

    def testBug(self):
        paths = File("wiki.dirs")
        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("/TESTSTATIC/htmlTest.html")
        TEST_EQ("", wikiName)
        TEST_EQ("STATIC", fileType)
        TEST_EQ("TESTSTATIC/htmlTest.html", pageName)

    def testStripQueryString(self):
        paths = FileFromList(
            [
                "WIKI wiki/*",
                "PLAIN plains/*.html\n",
                "STATIC statics/*.html\n",
                "WIKI top *",
            ]
        )

        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("/wiki/Page?this=that")
        TEST_EQ("wiki", wikiName)
        TEST_EQ("WIKI", fileType)
        TEST_EQ("wiki/Page", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("?this=that")
        TEST_EQ("top", wikiName)
        TEST_EQ("WIKI", fileType)
        TEST_EQ("WelcomePage", pageName)

        wikiName, fileType, pageName = matcher.pathInfo("/?this=that")
        TEST_EQ("top", wikiName)
        TEST_EQ("WIKI", fileType)
        TEST_EQ("WelcomePage", pageName)

    def testDefaultWikiPage(self):
        paths = FileFromList(
            [
                "WIKI wiki/*",
            ]
        )

        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("/wiki/")
        TEST_EQ("WIKI", fileType)
        TEST_EQ("wiki/WelcomePage", pageName)
        TEST_EQ("wiki", wikiName)

        wikiName, fileType, pageName = matcher.pathInfo("/wiki")
        TEST_EQ("WIKI", fileType)
        TEST_EQ("wiki/WelcomePage", pageName)
        TEST_EQ("wiki", wikiName)

    def testDefaultStaticPage(self):
        paths = FileFromList(
            [
                "PLAIN sbml/*.html",
                "STATIC *",
            ]
        )

        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("")
        TEST_EQ("STATIC", fileType)
        TEST_EQ("index.html", pageName)
        TEST_EQ("", wikiName)

        wikiName, fileType, pageName = matcher.pathInfo("/")
        TEST_EQ("STATIC", fileType)
        TEST_EQ("index.html", pageName)
        TEST_EQ("", wikiName)

        wikiName, fileType, pageName = matcher.pathInfo("sbml")
        TEST_EQ("PLAIN", fileType)
        TEST_EQ("sbml/index.html", pageName)
        TEST_EQ("", wikiName)

        wikiName, fileType, pageName = matcher.pathInfo("sbml/")
        TEST_EQ("PLAIN", fileType)
        TEST_EQ("sbml/index.html", pageName)
        TEST_EQ("", wikiName)

    def testDeepPath(self):
        paths = FileFromList(["STATIC statics//*.html"])

        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("statics/dir1/dir2/index.html")
        TEST_EQ("STATIC", fileType)
        TEST_EQ("statics/dir1/dir2/index.html", pageName)
        TEST_EQ("", wikiName)

        wikiName, fileType, pageName = matcher.pathInfo("statics/dir1/dir2/")
        TEST_EQ("STATIC", fileType)
        TEST_EQ("statics/dir1/dir2/index.html", pageName)
        TEST_EQ("", wikiName)

        wikiName, fileType, pageName = matcher.pathInfo("statics/dir1/dir2")
        TEST_EQ("STATIC", fileType)
        TEST_EQ("statics/dir1/dir2/index.html", pageName)
        TEST_EQ("", wikiName)

        """
      wikiName, fileType, pageName = \
         matcher.pathInfo("statics/dir1/dir2/file.bad")
      TEST_EQ("statics/dir1/dir2/file.bad", pageName)
      TEST_EQ("BAD", fileType)
      TEST_EQ("", wikiName)
      """

    def testExplicitHost(self):
        paths = FileFromList(
            [
                "WIKI lenore-exegesis http://lenore-exegesis.com/*",
                "WIKI another-wiki http://another-wiki.com/*",
            ]
        )

        matcher = PathMatch(paths)

        wikiName, fileType, pageName = matcher.pathInfo("SomePage", "another-wiki.com")
        TEST_EQ("WIKI", fileType)
        TEST_EQ("SomePage", pageName)
        TEST_EQ("another-wiki", wikiName)

    def test_convertToRegexp(self):
        TEST_EQ("blah\.html$", _convertToRegexp("blah.html"))
        TEST_EQ("[^/]+\.html$", _convertToRegexp("*.html"))
        TEST_EQ("statics/(.+/)*[^/]+\.html$", _convertToRegexp("statics//*.html"))

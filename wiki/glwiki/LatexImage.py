import os, re, shelve, cgi

# from fcntl import lockf, LOCK_EX, LOCK_UN

from Config import config
from ShellCommand import ShellCommand

databasename = "wiki.latexImageNames"
filenamePattern = re.compile(r"latex\d\d\d\.jpg")
lockFilename = "wiki.LATEX.CACHE.LOCK"
database = None

latexTemplate = r"""\documentclass[10pt,notitlepage]{article}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage[all]{xy}
\begin{document}
\pagestyle{empty}
%s
\end{document}
"""

insecureCommands = [
    re.compile(s)
    for s in [
        "newcommand",
        "renewcommand",
        "providecommand",
        "newenviroment",
        "renewenvironment",
        "input",
        "include",
        "includeonly",
        "listfiles",
        "begin.*\{.*filecontents",
        "typeout",
        "typein",
        "includegraphics",
        "newtheorem",
        "usepackage",
    ]
]


def clearLatexImages():
    global database
    for filename in os.listdir("."):
        if filenamePattern.match(filename):
            os.unlink(filename)

    del database
    database = None
    forceRemove(databasename)
    forceRemove(lockFilename)


def forceRemove(filename):
    try:
        os.unlink(filename)
    except OSError:
        pass
    assert not os.access(filename, os.F_OK)


class LatexImage:

    def __init__(self, repository, latexString):
        self._repository = repository
        self._latexString = latexString

    def __str__(self):
        if self._isInsecure():
            self._output = (
                "&lt;&lt;&lt;Sorry, but %s contains an insecure LaTeX command.&gt;&gt;&gt;"
                % self._latexString
            )
        else:
            self._getDatabase().lock()

            needToGenerate, imageFilename = self._getImageFilename()
            if needToGenerate:
                self._output = self._renderLatex(imageFilename)
            else:
                self._output = self._makeImg(imageFilename)

            self._getDatabase().unlock()

        return self._output

    def _getImageFilename(self):
        return self._getDatabase().getImageFilename(self._latexString)

    def _getDatabase(self):
        global database
        if database == None:
            database = LatexDatabase()
        return database

    def _makeCommands(self, imageFilename):
        return [
            ShellCommand("pdflatex expr.tex"),
            ShellCommand(
                "gs -dSAFER -dDOINTERPOLATE -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dNOPAUSE -r110x110 -sDEVICE=pnggray -sOutputFile=expr.png expr.pdf"
            ),
            ShellCommand("mogrify -crop 00x00+2+2 -format jpg expr.png"),
            ShellCommand("mv expr.jpg %s" % imageFilename),
        ]

    def _runCommands(self, imageFilename):
        for command in self._makeCommands(imageFilename):
            command.run()
            if command.getResult() != 0:
                return 0, command

        return 1, None

    def _renderLatex(self, imageFilename):
        f = file("expr.tex", "w")
        f.write(latexTemplate % self._latexString)
        f.close()

        succeeded, failedCommand = self._runCommands(imageFilename)

        if succeeded:
            self._getDatabase().imageFileCreated(self._latexString)
            return self._makeImg(imageFilename)
        else:
            return (
                "&lt;&lt;LaTeX failure:<PRE>command: %s\n\nreturned: %s\n</PRE>&gt;&gt;"
                % (
                    cgi.escape(failedCommand.getCommand()),
                    cgi.escape(failedCommand.getStdout()),
                )
            )

    def _makeImg(self, imageFilename):
        return '<IMG CLASS="latex-image" SRC="%s">' % config.makeUrl(
            self._repository.getWikiName(), imageFilename
        )

    def _isInsecure(self):
        for regexp in insecureCommands:
            if regexp.search(self._latexString):
                return True

        return False


class LatexDatabase:

    NextId = "n"  # key of "next" id number to assign
    prefix = "|"  # prefix for all strings, to distinguish them from NextId

    def __init__(self):
        self.shelf = shelve.open(databasename)

        if not self.shelf.has_key(LatexDatabase.NextId):
            self.shelf[LatexDatabase.NextId] = 0

    def __getattr__(self, name):
        if name != "_lockFile":
            raise AttributeError(name)
        else:
            self._lockFile = open(lockFilename, "a")
            return self._lockFile

    def lock(self):
        # lockf(self._lockFile, LOCK_EX)
        pass

    def unlock(self):
        # lockf(self._lockFile, LOCK_UN)
        pass

    def getImageFilename(self, s):
        """returns (needToGenerate, filename) where needToGenerate is
        a true/false flag telling whether the image file needs to be
        created."""

        s = LatexDatabase.prefix + s
        if self.shelf.has_key(s):
            return 0, self._makeFilename(self.shelf[s])
        else:
            return 1, self._makeFilename(self._getNextId())

    def imageFileCreated(self, latexString):
        self.shelf[LatexDatabase.prefix + latexString] = self._getNextId()
        self._bumpNextId()

    def _getNextId(self):
        return self.shelf[LatexDatabase.NextId]

    def _bumpNextId(self):
        newId = self._getNextId() + 1
        if newId >= 1000:
            newId = 0
        self.shelf[LatexDatabase.NextId] = newId

    def _makeFilename(self, n):
        return "latex%03d.jpg" % n

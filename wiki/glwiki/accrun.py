#! /usr/bin/env python

# accrun.py:
#    acceptance-test runner: runs a test listed on the command line

# The test file contains a command to run and a regular expression that
# matches passing output.

# TROUBLESHOOTING: if it sure seems that the 'expect' string should match
# the 'got' string, try running re.escape() on most or all of the 'expect'
# string.  The 'expect' string might contain regular-expression
# metacharacters.

import sys, os, re

ST_START = 0
ST_IN_EXPECT = 1

class Main:

   def __init__(self):
      self.runAndCompare(self.getCommandLineArgument())


   def runAndCompare(self, filename):
      self.parseTestDescriptionFile(filename)
      self.expectRe = re.compile(self.expect, re.MULTILINE | re.DOTALL)
      (nullStdin, self.commandOutput) = os.popen4(self.command)
      nullStdin.close()
      self.got = self.commandOutput.read()

      if self.expectRe.match(self.got):
         print "%-30s PASSED" % filename
      else:
         print "%-30s FAILED  (see %s and %s)" % (
            filename,
            self.errorExpectFilename(filename),
            self.errorGotFilename(filename),
         )

         expectFile = file(self.errorExpectFilename(filename), "w")
         expectFile.write(self.expect)
         expectFile.close()

         gotFile = file(self.errorGotFilename(filename), "w")
         gotFile.write(self.got)
         gotFile.close()

         sys.exit(1)
      

   def parseTestDescriptionFile(self, filename):
      testDescriptionFile = self.openFile(filename)

      self.command = ""
      self.expect = ""
      
      state = ST_START
      for line in testDescriptionFile:
         if state == ST_START:
            if line.startswith("----"):
               state = ST_IN_EXPECT
            else:
               self.command += line
         else:
            self.expect += line

      if state != ST_IN_EXPECT:
         errorExit(filename + " does not contain 'expect' portion")


   def openFile(self, filename):
      try:
         return file(filename, "r")
      except IOError, e:
         errorExit(e)


   def removeOutputFile(self, filename):
      filename = self.outputFilename(filename)
      try:
         os.unlink(filename)
      except OSError:
         pass
      assert not os.access(filename, os.F_OK)


   def errorExpectFilename(self, filename):
      return os.path.basename(filename) + ".expected"


   def errorGotFilename(self, filename):
      return os.path.basename(filename) + ".got"


   def getCommandLineArgument(self):
      if len(sys.argv) != 2:
         usage()
      else:
         return sys.argv[1]


def errorExit(exception):
   print >>sys.stderr, "%s: %s" % (sys.argv[0], str(exception))
   sys.exit(2)


def usage():
   print >>sys.stderr, \
"""usage: accrun.py expectFile gotFile

If gotFile is -, compares expectFile against standard input."""
   sys.exit(2)


Main()

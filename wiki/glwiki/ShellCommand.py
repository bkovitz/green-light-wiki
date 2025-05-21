# import os
# from popen2 import Popen4
#
#
# class ShellCommand:
#
#   def __init__(self, commandString):
#      self._commandString = commandString
#
#
#   def run(self):
#      p = Popen4(self._commandString, 1)
#      p.tochild = None  # stdin is nothing but EOF
#      self._exitCode = p.wait() >> 8
#      self._stdout = p.fromchild.read()
#
#
#   def getCommand(self):
#      return self._commandString
#
#
#   def getResult(self):
#      return self._exitCode
#
#
#   def getStdout(self):
#      return self._stdout

import os
import subprocess


class ShellCommand:
    def __init__(self, commandString):
        self._commandString = commandString

    def run(self):
        # Use subprocess instead of popen2 (which is removed in Python 3)
        process = subprocess.Popen(
            self._commandString,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=False,
        )

        # Send EOF to stdin
        process.stdin.close()

        # Get output and exit code
        self._stdout = process.stdout.read()
        self._exitCode = process.wait()

    def getCommand(self):
        return self._commandString

    def getResult(self):
        return self._exitCode

    def getStdout(self):
        return self._stdout

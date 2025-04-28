#!/usr/bin/python

"""
Green Light Wiki
"""

import os, sys
from traceback import print_exc
from time import asctime

from CommandLine import cmdArgs
from Environments import getEnvironment
from PathMatch import PathMatch
from File import File
from Log import log
from Chunks import setChunkFile
from SocketServer import SocketServer
from WikiClient import socketTransaction
from Misc import forceRemove


import time

class Lo:
   def __init__(self):
      self.f = open("dates", "a")

   def __call__(self, msg):
      #print >>self.f, time.strftime("%a %d-%b-%Y %H:%M:%S"), msg
      print(time.strftime("%a %d-%b-%Y %H:%M:%S"), msg, file=self.f)
      self.f.flush()

lo = Lo()


socketAddress = "wiki.socket"

class Main:
   def __init__(self):
      if cmdArgs.command == "RESIDE":
         server = SocketServer(socketAddress, wikiService)
      elif cmdArgs.command == "TERMINATE":
         socketTransaction(socketAddress, "terminate\n")
      elif cmdArgs.command == "TEST":
         print("Main.py TEST")
         print(socketTransaction(socketAddress, "test\n"))
      else:
         print(serveWikiCommand(cmdArgs, os.environ, sys.stdin))

   '''
   def __del__(self):
      print "__del__" #DEBUG
      forceRemove(socketAddress)
   '''


def serveWikiCommand(cmdArgs, environ, stdin):
   lo("serveWikiCommand")
   environment = getEnvironment(
      cmdArgs,
      environ,
      File("wiki.dirs"),
      stdin
   )
   lo("getEnvironment")

   requestedPage = environment.getRequestedPage()
   lo("getRequestedPage")

   setChunkFile(environment.getWikiName())
   lo("getWikiName")

   requestedPage.action()
   lo("action")

   log(
      os.environ,
      requestedPage.getCommand(),
      environment.getUri(),
      environment.getUserName()
   )
   lo("log")

   result = requestedPage.renderCgi()
   lo("renderCgi")

   return result


def wikiService(environ, stdin):
   return serveWikiCommand(None, environ, stdin)


try:
   Main()
except:
   print("Content-type: text/plain\n")

   print_exc(None, sys.stdout)

   logFile = open("wiki.tracebacks", "a")
   #print >>logFile, asctime()
   print(asctime(), file=logFile)
   envvars = os.environ.keys()[:]
   envvars.sort()
   for envvar in envvars:
      #print >>logFile, "%s=%s" % (envvar, os.environ[envvar])
      print("%s=%s" % (envvar, os.environ[envvar]), file=logFile)
   print_exc(None, logFile)
   print(file=logFile)
   logFile.close()

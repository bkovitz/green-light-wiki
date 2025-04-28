from re import match
from http.cookies import SimpleCookie
from random import randrange
from time import time

from Config import config
from HashFile import HashFile


sessionDatabase = HashFile("wiki.sessions")
pendingMessages = HashFile("wiki.messages")


class BadSessionId(Exception):

   def __init__(self, id):
      self.id = id

   def __str__(self):
      return 'unknown session id: "%s"' % self.id


def makeSession(startTime, ipAddress):
   id = _makeId()
   sessionDatabase[id] = ipAddress
   return id


def getUserName(id):
   try:
      return sessionDatabase[id]
   except KeyError:
      return "(unknown)"


def setUserName(id, newUserName):
   if id not in sessionDatabase:
      raise BadSessionId(id)
   sessionDatabase[id] = newUserName


def getPendingMessage(id, retrievalTime=None):
   if retrievalTime is None:
      retrievalTime = time()

   try:
      messageChunkClass, pageTitle, postTime = pendingMessages[id]
   except KeyError:
      return (None, None)

   if postTime is None or postTime + 10 >= retrievalTime:
      return (messageChunkClass, pageTitle)
   else:
      return (None, None)


def setPendingMessage(id, messageChunkClass, pageTitle, postTime=None):
   pendingMessages[id] = (messageChunkClass, pageTitle, postTime)


def makeCookie(id):
   result = SimpleCookie()
   result["wiki-session"] = id
   morsel = result["wiki-session"]
   #TODO: intelligent defaults if nothing is defined in wiki.config
   morsel["domain"] = config.get("", "cookie domain")
   morsel["path"] = config.get("", "cookie path")
   morsel["max-age"] = 15552000  # 180 days
   morsel["version"] = 1
   return result


def isLoggedIn(id):
   if not id:
      return 0

   userName = getUserName(id)
   return (
      userName != "(unknown)"
      and
      not match("\d+\.\d+\.\d+\.\d+", userName)
   )


_sessionIdChars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
def _makeId():
   result = ""
   r = len(_sessionIdChars)
   for i in range(20):
      result += _sessionIdChars[randrange(r)]

   return result



import os


def stripLeadingSlash(uri):
   if uri and uri[0] == "/":
      return uri[1:]
   else:
      return uri


def makeList(thing):
   if isinstance(thing, list):
      return thing
   elif isinstance(thing, tuple):
      return list(thing)
   elif thing is None:
      return []
   else:
      return [thing]


def forceRemove(filename):
   try:
      os.unlink(filename)
   except OSError:
      pass
   assert not os.access(filename, os.F_OK)

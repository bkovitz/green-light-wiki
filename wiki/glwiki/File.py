import os, sys

from Config import config
from Misc import makeList

class File:

   def __init__(self, filename):
      self.filename = filename
      self._open()


   def _open(self):
      try:
         self._f = open(self.filename, "r")
         self._exists = 1
      except IOError:
         self._f = None
         self._exists = 0


   def exists(self):
      return self._exists

   
   def __iter__(self):
      if self._f:
         self.rewind()
         return iter(self._f)
      else:
         return iter([])


   def readlines(self):
      if self._f:
         self.rewind()
         return self._f.readlines()
      else:
         return []


   def close(self):
      if self._f:
         self._f.close()


   def rewind(self):
      try:
         self._f.seek(0)
      except IOError:
         pass


class NonwikiFile(File):

   def __init__(self, filename):
      File.__init__(self, config.getNonwikiFilename(filename))


class PipeFrom(File):

   def __init__(self, prog, env, *args):
      self.filename = prog
      self._env = env
      self._args = makeList(args)

      self._open()


   def _open(self):
      self._f = self._openPipe()
      self._exists = 1


   def _openPipe(self):
      r, w = os.pipe()

      if os.fork() == 0:   # if child process
         os.close(r)
         os.dup2(w, 1)     # child process's stdout goes through pipe
         try:
            os.execvpe(
               self.filename,
               [self.filename] + self._args,
               self._env
            )
         except OSError:
            sys.exit(2)

      else:                # else parent process
         os.close(w)
         return os.fdopen(r)

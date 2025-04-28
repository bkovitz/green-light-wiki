import io


class TextFile:

   """Lets you operate on a file as it exists on disk, without thinking about
   whether it's open or even if it exists.  Not suitable for large text files:
   we always read the entire file into memory.  Also, assumes that the file is
   unchanged on disk in between writes.
   """


   def __init__(self, filename):
      self._filename = filename
      self._content = None
      self._lines = None
      self._dirty = False


   def __str__(self):
      self._readContentIfNecessary()
      return self._content

      
   def lines(self):
      self._readLinesIfNecessary()
      return self._lines


   def write(self, entireNewFileContents):
      if isinstance(entireNewFileContents, list):
         entireNewFileContents = "\n".join(entireNewFileContents + [""])

      # TODO Understand why io.open was necessary; open() appears to be lost
      # from builtins.
      f = io.open(self._filename, "w")
      f.write(entireNewFileContents)
      del f


   def __del__(self):
      if self._dirty:
         self.write(self._lines)


   def __getitem__(self, key):
      self._readLinesIfNecessary()
      try:
         return self._lines[key]
      except IndexError:
         return ""


   def __setitem__(self, key, value):
      self._readLinesIfNecessary()

      if key < len(self._lines):
         self._lines[key] = str(value)
      else:
         self._lines += [""] * (len(self._lines) - key)
         self._lines.append(str(value))

      self._content = None
      self._dirty = True


   def __iter__(self):
      return self.lines().__iter__()


   def __eq__(self, other):
      return str(self) == str(other)


   def __ne__(self, other):
      return not str(self) == str(other)


   def _readLinesIfNecessary(self):
      if self._lines is None:
         self._readLines()


   def _readLines(self):
      self._readContentIfNecessary()
      self._lines = self._content.splitlines()


   def _readContentIfNecessary(self):
      if self._dirty:
         self._content = "\n".join(self._lines + [""])
      else:
         if self._content is None:
            self._readContent()


   def _readContent(self):
      try:
         #f = open(self._filename, "r")
         f = open(self._filename, "r")
      except IOError:
         self._content = ""
         return

      self._content = f.read()
      del f

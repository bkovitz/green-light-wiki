import sys


class CommandLine:

   def __init__(self, argv):
      argv = argv[:]

      self.wikiName = None
      self.buttons = 1
      self.command = "APACHE"

      self._alreadyGotCommand = 0
      self._okFlag = 1
      self._errorMessage = None

      if len(argv):
         del argv[0]

      while argv:
         arg = argv[0]
         if arg.startswith("--"):
            if arg[2:] == "nobuttons":
               self.buttons = 0
            else:
               self._fail("unrecognized switch: " + arg)
               break
         else:
            if _isCommand(arg):
               if self._alreadyGotCommand:
                  self._fail("more than one command on command line")
               else:
                  self.command = arg
                  self._alreadyGotCommand = 1
            else:
               if self.wikiName:
                  self._fail("more than one wiki name on command line")
               else:
                  self.wikiName = arg
            """
            if self.wikiName:
               if _isCommand(arg):
                  self.command = arg
               else:
                  self._fail("unknown command: " + arg)
            else:
               self.wikiName = arg
            """

         del argv[0]


   def ok(self):
      return self._okFlag


   def errorMessage(self):
      return self._errorMessage


   def _fail(self, msg):
      self._okFlag = 0
      self._errorMessage = msg


commands = [ "APACHE", "STATIC", "RESIDE", "TERMINATE", "TEST" ]
def _isCommand(arg):
   return arg in commands


cmdArgs = CommandLine(sys.argv)

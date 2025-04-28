from teest import *

from CommandLine import CommandLine

class ut_ParseCommandLine:

   def testOneArgument(self):
      argv = [ "Main.py", "wikiname" ]

      cmdArgs = CommandLine(argv)

      TEST_EQ("APACHE", cmdArgs.command)
      TEST_EQ("wikiname", cmdArgs.wikiName)
      TEST(cmdArgs.buttons)
      TEST(cmdArgs.ok())


   def testNoArguments(self):
      argv = [ "Main.py" ]

      cmdArgs = CommandLine(argv)

      TEST_EQ("APACHE", cmdArgs.command)
      TEST_EQ(None, cmdArgs.wikiName)
      TEST(cmdArgs.buttons)
      TEST(cmdArgs.ok())


   def testNoButtonsWithoutWiki(self):
      argv = [ "Main.py", "--nobuttons" ]

      cmdArgs = CommandLine(argv)

      TEST_EQ("APACHE", cmdArgs.command)
      TEST_EQ(None, cmdArgs.wikiName)
      TEST(not cmdArgs.buttons)
      TEST(cmdArgs.ok())


   def testNoButtonsWithWiki(self):
      argv = [ "Main.py", "--nobuttons", "wik" ]

      cmdArgs = CommandLine(argv)

      TEST_EQ("APACHE", cmdArgs.command)
      TEST_EQ("wik", cmdArgs.wikiName)
      TEST(not cmdArgs.buttons)
      TEST(cmdArgs.ok())


   def testStaticWithWiki(self):
      argv = [ "Main.py", "wik", "STATIC" ]
      
      cmdArgs = CommandLine(argv)

      TEST_EQ("STATIC", cmdArgs.command)
      TEST_EQ("wik", cmdArgs.wikiName)
      TEST(cmdArgs.ok())


   def testStaticWithoutWiki(self):
      argv = [ "Main.py", "STATIC" ]
      
      cmdArgs = CommandLine(argv)

      TEST_EQ("STATIC", cmdArgs.command)
      TEST_EQ(None, cmdArgs.wikiName)
      TEST(cmdArgs.ok())


   def testBadSwitch(self):
      argv = [ "Main.py", "--crazy" ]

      cmdArgs = CommandLine(argv)

      TEST(not cmdArgs.ok())
      TEST(cmdArgs.errorMessage())


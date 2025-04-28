from teest import *

from ShellCommand import ShellCommand


class ut_ShellCommand:

   def testSimple(self):
      cmd = ShellCommand('echo "some text"')

      cmd.run()

      TEST_EQ(0, cmd.getResult())
      TEST_EQ("some text\n", cmd.getStdout())


   def testNoncommand(self):
      cmd = ShellCommand('not-a-real-command')

      cmd.run()

      TEST_NE(0, cmd.getResult())
      TEST(len(cmd.getStdout()) > 0)


   def testCommandThatReadsFromStdin(self):
      cmd = ShellCommand("cat > /dev/null")

      cmd.run()

      TEST_EQ(0, cmd.getResult())

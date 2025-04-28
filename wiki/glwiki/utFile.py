from teest import *

from File import PipeFrom

class ut_File:

   def testPipeFrom(self):
      env = {
         "ENV_VAR": "test value",
         "PATH": "./TESTSTATIC:/bin:/usr/bin"
      }
      f = PipeFrom("pipetest.sh", env, "first arg", "second arg")

      got = [ line.rstrip() for line in f.readlines() ]

      expect = [
         "Pipetest output",
         "first arg",
         "second arg",
         "ENV_VAR=test value",
         # "PATH=./TESTSTATIC:/bin:/usr/bin",  (fails under Cygwin)
      ]

      TEST_EQ(expect, got[:len(expect)])
      TEST_EQ("end", got[-1])

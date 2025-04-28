from teest import *
from Misc import forceRemove
from TextFile import TextFile

from HashFile import HashFile

      
testFileName = "TESTDATA/hashfile"


class ut_HashFile:

   def setUp(self):
      forceRemove(testFileName)


   def tearDown(self):
      forceRemove(testFileName)


   def testPut(self):
      hash = HashFile(testFileName)
      hash["key"] = "value"
      del hash

      TEST_EQ("key,value\n", TextFile(testFileName))


   def testGet(self):
      hash = HashFile(testFileName)
      hash["key"] = "value"
      del hash
   
      hash = HashFile(testFileName)
      TEST_EQ("value", hash["key"])
      del hash


   def testContains(self):
      hash = HashFile(testFileName)
      hash["goodkey"] = "value"

      TEST("goodkey" in hash)
      TEST("badkey" not in hash)


   def testTrickyValue(self):
      TextFile(testFileName).write("m8zjXBLmom70Kyp4SP7v,\"(<class Chunks.SuccessfulSaveChunk at 0x240b10>, 'Page Title', 1065046739)\"")

      hash = HashFile(testFileName)
      # no exception means test passed

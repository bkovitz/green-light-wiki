from teest import *

class ut_SomeClass:

   def testTestEqTrue(self):
      TEST_EQ("a" , "a")

   def testTestEqFalse(self):
      TEST_EQ("a" , "b")
      
   def testTestNeTrue(self):
      TEST_NE("a", "b")
      
   def testTestNeFalse(self):
      TEST_NE("a", "a")

   def testTrue(self):
      TEST(1)

   def testFalse(self):
      TEST(0)

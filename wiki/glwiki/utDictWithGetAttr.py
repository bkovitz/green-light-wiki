from teest import *

from DictWithGetAttr import DictWithGetAttr

class ut_DictWithGetAttr:

   def testAll(self):
      class Thing:
         def __init__(self):
            self.attr = "abc"

         def __getattr__(self, name):
            if name == "other":
               return "it works"
            else:
               raise NameError(name)

      d = DictWithGetAttr(Thing())

      TEST_EQ("abc", d["attr"])
      TEST_EQ("it works", d["other"])
      TEST_EXC(NameError, lambda: d["nonexistent"])

from teest import *

from RequestedPage import RequestedPage

class InstanceClass(RequestedPage):

   def renderHtml(self):
      self._cgiLeader = "blah\n"
      return "some html\n"

   def cgiLeader(self):
      return self._cgiLeader


class ut_RequestedPage:

   def testRenderCgi(self):
      page = InstanceClass()

      expect = \
"""blah

some html
"""
      TEST_EQ(expect, page.renderCgi())

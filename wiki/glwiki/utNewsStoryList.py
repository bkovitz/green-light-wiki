from teest import *
from utMisc import FileFromList

from NewsStory import NewsStory
from NewsStoryList import NewsStoryList

class ut_NewsStoryList:

   def testGetTop3(self):
      file1 = FileFromList([
         "First story",
         "Aug 12, 2003",
         "Some text",
      ])
      
      file2 = FileFromList([
         "Second story",
         "Aug 14, 2003",
         "Some more text",
      ])
      
      file3 = FileFromList([
         "Third story",
         "August 15, 2003",
         "Text some more",
      ])
      
      file4 = FileFromList([
         "Fourth story",
         "17-Aug-2003",
         "Yet more text",
      ])

      stories = [ NewsStory(file) for file in [file2, file3, file4, file1] ]

      expect = [
         "Fourth story",
         "Third story",
         "Second story",
      ]

      storyList = NewsStoryList(stories)
      got = [
         story.getTitle()
            for story in storyList.allStoriesSince("14-Aug-2003")
      ]

      TEST_EQ(expect, got)

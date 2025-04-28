from teest import *
from utMisc import FileFromList

from NewsStory import NewsStory
from StoryRectangle import StoryRectangle


class ut_NewsStory:

   def testAll(self):
      storyFile = FileFromList([
         "Exciting Things Happen",
         "September 25, 2003",
         "",
         "Today, four exciting things happened.  The first one was pretty",
         "exciting.  The second one was very exciting.  The third one",
         "excited a crowd of onlookers.  The fourth one was indescribably",
         "exciting, but only to people with exceptionally refined tastes.",
      ])

      story = NewsStory(storyFile)

      TEST_EQ("Exciting Things Happen", story.getTitle())
      TEST_EQ("September 25, 2003", str(story.getDate()))

      expect = [
         "Today, four exciting things happened.  The first one was pretty",
         "exciting.  The second one was very exciting.  The third one",
         "excited a crowd of onlookers.  The fourth one was indescribably",
         "exciting, but only to people with exceptionally refined tastes.",
      ]
      TEST_EQ(expect, story.getBody())


   def testSummary(self):
      storyFile = FileFromList([
         "Iceberg Discovered",
         "September 25, 2003",
         "",
         "The first paragraph is the summary.",
         "It might extend to multiple lines.",
         "",
         "The second paragraph."
      ])

      story = NewsStory(storyFile)

      expect = [
         "The first paragraph is the summary.",
         "It might extend to multiple lines.",
      ]

      TEST_EQ(expect, story.getSummary())


   def testSummaryIntoRectangle(self):
      storyFile = FileFromList([
         "Iceberg Discovered",
         "September 25, 2003",
         "",
         "The first paragraph is the summary.",
         "It might extend to multiple lines.",
         "",
         "The second paragraph."
      ])

      story = NewsStory(storyFile)

      expect = \
"""<H1>Iceberg Discovered</H1>
<P><SPAN CLASS="date">(September 25, 2003)</SPAN> The first paragraph is the summary.
It might extend to multiple lines.</P>
"""
      got = story.getSummaryRectangle()

      TEST_EQ(StoryRectangle, got.__class__)
      TEST_EQ(expect, "".join([str(item) for item in got.getItems()]))

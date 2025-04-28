from Date import Date


class NewsStoryList:

   def __init__(self, stories):
      self._stories = stories


   def allStoriesSince(self, since):
      since = Date(since)
      result = [
         story for story in self._stories if story.getDate() >= since
      ]
      result.sort(  # sort into reverse chronological order
         lambda s1, s2: cmp(s2.getDate(), s1.getDate())
      )

      return result

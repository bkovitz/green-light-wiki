class DictWithGetAttr:

   def __init__(self, object):
      self.object = object


   def __getitem__(self, index):
      try:
         return self._fetchFromDictionaryOrGetAttr(index)
      except AttributeError:
         return None

   def _fetchFromDictionaryOrGetAttr(self, index):
      try:
         return self.object.__dict__[index]
      except KeyError:
         return self.object.__getattr__(index)

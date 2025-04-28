import re

def unsmashWords(smashedWord):
   if "_" not in smashedWord:
      if not len(smashedWord) or not smashedWord[0].isupper():
         return smashedWord
      words = re.findall("([A-Z][a-z0-9]*)", smashedWord)
      words = _mergeConsecutiveSingleCapitalLetters(words)
      return " ".join(words)
   else:
      return smashedWord.replace("_", " ").strip()


def _mergeConsecutiveSingleCapitalLetters(words):
   result = []

   for word in words:
      if (
         len(result) >= 1
         and
         result[-1].isupper()
         and (
            word.isupper()
            or
            _isCapWithPlural(word)
         )
      ):
         result[-1] += word
      else:
         result.append(word)

   return result


def _isCapWithPlural(word):
   return re.match("[A-Z]s", word)

import time, shelve, re
from copy import deepcopy

from WikiRepository import WikiRepository
from Config import config
from Html import HtmlAnchor, HtmlHolder, HtmlPara, H2
from UnsmashWords import unsmashWords
from HtmlMisc import _itemClass

nextId = "/nextId"


class MostRecentChangeToAPage:

   def __init__(self, pageName, userName, date=None):
      self.pageName = pageName
      self.userName = userName
      self.index = None

      if not date:
         self.date = int(time.time())
      else:
         self.date = int(date)


   def write(self, d):
      self.index = _nextSequentialKey(d)
      d[_indexKey(self.index)] = self
      d[self.pageName] = self


   def delete(self, d):
      del d[_indexKey(self.index)]
      del d[self.pageName]


def logChange(command):  #TODO: delete this
   logChange2(command.wikiName, command.userName, command.pageName)


def logChange2(wikiName, userName, pageName):
   with shelve.open(_shelfName(wikiName)) as d:

    #  if d.has_key(pageName):
    if pageName in d:
        change = d[pageName]
        change.delete(d)
        change.userName = userName
        change.date = int(time.time())
        change.write(d)
    else:
        change = MostRecentChangeToAPage(pageName, userName)
        change.write(d)

    #    d.close()


def retrieveChanges(wikiName, numRecords):
   """
      MostRecentChangeToAPage's are returned in reverse chronological order
   """
   with shelve.open(_shelfName(wikiName)) as d:

       result = []
       maxKey = _maxKey(d)
       while len(result) < numRecords and maxKey >= 1:
           if _indexKey(maxKey) in d:
               result.append(d[_indexKey(maxKey)])
           maxKey -= 1

   return result


def render(wikiName):
   return _renderChanges(retrieveChanges(wikiName, 50))


def renderHtml(wikiName):
   return _renderChangesInHtml(retrieveChanges(wikiName, 50), wikiName)


def _renderChangesInHtml(changes, wikiName):
   result = HtmlHolder()
   prevYear = prevMonth = prevDay = None

   for change in changes:
      timeTuple = time.localtime(change.date)
      year, month, day, hours, minutes, ignored, dow = timeTuple[:7]

      if year != prevYear or month != prevMonth or day != prevDay:
         result.add(H2(
            "%s, %s %d" % (
               _dayNames[dow],
               _monthNames[month],
               day
            )
         ))
         prevYear = year
         prevMonth = month
         prevDay = day

      result.add(HtmlPara(
         "%02d:%02d %s . . . . . . %s" % (
            hours,
            minutes,
            _makeUrl(wikiName, change.pageName),
            _makeUrl(wikiName, change.userName),
         ),
         _itemClass
      ))

   return result


def _makeUrl(wikiName, pageName):
   if re.match("^[0-9.]+$", pageName):
      return pageName
   else:
      return HtmlAnchor(
         config.makeUrl(wikiName, pageName),
         unsmashWords(pageName)
      )


def _renderChanges(changes):
   result = ""
   prevYear = prevMonth = prevDay = None

   for change in changes:
      timeTuple = time.localtime(change.date)
      year, month, day, hours, minutes, ignored, dow = timeTuple[:7]

      # TODO: fix OAOO
      if year != prevYear or month != prevMonth or day != prevDay:
         result += "%s, %s %d\n\n" % (_dayNames[dow], _monthNames[month], day)
         prevYear = year
         prevMonth = month
         prevDay = day

      result += " %02d:%02d [%s] . . . . . . [%s]\n" % (
         hours,
         minutes,
         change.pageName,
         change.userName
      )

   return result


def _row(contents):
   return HtmlRow(HtmlDatum(contents))


def _shelfName(wikiName):
   return wikiName + ".RecentChanges"


def _nextSequentialKey(d): #TODO _newS..
   result = _maxKey(d) + 1
   d[nextId] = result + 1
   return result


def _maxKey(d):
   if d.has_key(nextId):
      return d[nextId] - 1
   else:
      return 0


def _indexKey(n):
   return "/" + str(n)


# needed only because time.strftime() insists on putting a leading zero before
# the day of the month

_monthNames = [
   "",
   "January",
   "February",
   "March",
   "April",
   "May",
   "June",
   "July",
   "August",
   "September",
   "October",
   "November",
   "December"
]

_dayNames = [
   "Monday",
   "Tuesday",
   "Wednesday",
   "Thursday",
   "Friday",
   "Saturday",
   "Sunday",
]

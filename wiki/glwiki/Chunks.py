#from io import StringIO
from io import StringIO

from HtmlChunk import HtmlChunkFromFile
from RecentChanges import _monthNames  #TODO: put timestamp class in its own place
from Config import config

_chunkFile = None


def setChunkFile(wikiName):
   global _chunkFile
   try:
      chunkFileName = config.get(wikiName, "html file", "wiki.html")
      _chunkFile = open(chunkFileName, "r")
   except IOError:
      _chunkFile = None


class GenericChunk(HtmlChunkFromFile):

   def __init__(self, page, chunkName, default):
      self.page = page
      HtmlChunkFromFile.__init__(self, _getChunkFile(), chunkName, default)


   def __getattr__(self, name):
      if name == "preambleBody":
         return self.preamble.body()
      elif name == "preambleLinks":
         return self.preamble.links()
      elif name == "preamble":
         return self.page.preamble()
      else:
         raise NameError(name)


   def isListBreak(self):
      return False


   def needsNumber(self):
      return False


def _getChunkFile():
   global _chunkFile
   if not _chunkFile:
      try:
         _chunkFile = open("wiki.html", "r")
      except IOError:
         _chunkFile = StringIO()

   return _chunkFile


class HtmlPageChunk(GenericChunk):

   def __init__(self, page, title, stylesheets, keywords, metas, body):
      self.title = title
      self.stylesheets = stylesheets
      self.keywords = keywords
      self.metas = metas
      self.body = body

      GenericChunk.__init__(self, page, "HtmlPage",
"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
  <title><%= title %></title>
  <%= preambleLinks %>
  <%= stylesheets %>
  <%= keywords %>
  <%= metas %>
  <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">
</head>
<body>
  <%= body %>
</body>
</html>
""")


class WikiPageBodyChunk(GenericChunk):

   def __init__(self, page, top, message, content, bottom):
      self.top = top
      self.message = message
      self.content = content
      self.bottom = bottom

      GenericChunk.__init__(self, page, "WikiPageBody",
"""<%= preambleBody %>
<%= top %>
<%= message %>
<%= content %>
<%= bottom %>
""")


class TopChunk(GenericChunk):

   def __init__(self, page, title, homeLink, logo=None):
      self.title = title
      self.homeLink = homeLink
      self.logo = logo

      GenericChunk.__init__(self, page, "Top",
"""<div id="wiki-top">
<%= logo %>
<p><%= homeLink %></p>
<h1><%= title %></h1>
</div>
""")


class BottomChunk(GenericChunk):

   def __init__(self, page, content):
      self.content = content

      GenericChunk.__init__(self, page, "Bottom",
"""<div id="wiki-buttons">
<%= content %>
</div>
""")


class ContentChunk(GenericChunk):

   def __init__(self, page, content):
      self.content = content

      GenericChunk.__init__(self, page, "Content",
"""<div id="wiki-content">
<%= content %>
</div>
""")


class EditChunk(GenericChunk):

   def __init__(self, page, text):
      self.text = text

      GenericChunk.__init__(self, page, "Edit",
"""<div id="wiki-edit">
  <textarea rows=24 cols=80 wrap=virtual name="text"><%= text %></textarea>
</div>
""")


class EditContentChunk(GenericChunk):

   def __init__(self, page, url, text, origVersionNum):
      self.url = url
      self.text = text
      self.origVersionNum = origVersionNum

      GenericChunk.__init__(self, page, "EditContent",
"""<div id="wiki-edit">
  <form action="<%= url %>" method=post><textarea rows=24 cols=80 wrap=virtual name="text"><%= text %></textarea>
<div id="wiki-edit-buttons">
    <input type=submit value=" Save "><input type=hidden name="origVersion" value="<%= origVersionNum %>">
  </div>
</form>
</div>
""")


class HorizontalRuleChunk(GenericChunk):

   def __init__(self, page):
      GenericChunk.__init__(self, page, "HorizontalRule", "<HR>")


class ListBreak:

   def isListBreak(self):
      return True


class NumberedListItem:

   def needsNumber(self):
      return True


# create a whole bunch of Chunk classes

textChunkClasses = {
   "Paragraph":         r'<p><%= text %></p>\n',
   "ChangedParagraph":  r'<p class="changed"><%= text %></p>\n',
   "Heading1":          r'<h1><%= text %></h1>\n',
   "ChangedHeading1":   r'<h1 class="changed"><%= text %></h1>\n',
   "Heading2":          r'<h2><%= text %></h2>\n',
   "ChangedHeading2":   r'<h2 class="changed"><%= text %></h2>\n',
   "Heading3":          r'<h3><%= text %></h3>\n',
   "ChangedHeading3":   r'<h3 class="changed"><%= text %></h3>\n',
   "Heading4":          r'<h4><%= text %></h4>\n',
   "ChangedHeading4":   r'<h4 class="changed"><%= text %></h4>\n',
   "Heading5":          r'<h5><%= text %></h5>\n',
   "ChangedHeading5":   r'<h5 class="changed"><%= text %></h5>\n',
   "UnorderedListItem":
      r'<table><tr><td class="bullet">&bull;<td><%= text %></td></tr></table>\n',
   "ChangedUnorderedListItem":
      r'<table class="changed"><tr><td class="bullet">&bull;<td><%= text %></td></tr></table>\n',
   "OrderedListItem":
      r'<table><tr><td class="bullet"><%= number %><td><%= text %></td></tr></table>\n',
   "ChangedOrderedListItem":
      r'<table class="changed"><tr><td class="bullet"><%= number %><td><%= text %></td></tr></table>\n',
}

fmtMakeClass = \
"""class %sChunk(%sGenericChunk):

   def __init__(self, page, text):
      self.text = text
      GenericChunk.__init__(self, page, "%s", "%s")
"""

for className in textChunkClasses.keys():
   template = textChunkClasses[className].replace('"', r'\"')

   if className.find("ListItem") < 0:
      preInherit = "ListBreak, "
   elif className.find("Ordered") >= 0:
      preInherit = "NumberedListItem, "
   else:
      preInherit = ""

   #exec fmtMakeClass % (className, preInherit, className, template)
   exec(fmtMakeClass % (className, preInherit, className, template))


class VersionInfoChunk(GenericChunk):

   def __init__(self, page, versionNum, date, author):
      self.versionNum = str(versionNum)
      self.date = friendlyDate(date)
      self.author = author

      GenericChunk.__init__(self, page, "VersionInfo",
"""<div class=\"version\">
  <p>Version <%= versionNum %> <%= date %></p>
  <p>Last edit by <%= author %></p>
</div>
""")


def friendlyDate(dateStringWithDots):
   try:
      year, month, day, hour, minute, ignored = [
         int(item) for item in dateStringWithDots.split('.')
      ]
   except ValueError:
      return "(unknown date)"

   return "%04d-%3s-%02d %02d:%02d %s" % (
      year,
      _monthNames[month][:3],
      day,
      hour,
      minute,
      "UTC"
   )


class Error404Chunk(GenericChunk):

   def __init__(self, page, url):
      self.url = url

      GenericChunk.__init__(self, page, "Error404",
"""<div id="wiki-message">
<h1>Page not found</h1>
<p>Error 404.</p>
<p>The requested resource, "<%= url %>", does not exist.</p>
<p>It is possible that you typed the URL incorrectly or that the
referring resource is out of date.</p>
</div>
""")


class BadVersionNumberChunk(GenericChunk):

   def __init__(self, page, versionNum):
      self.page = page
      self.pageName = page.getTitle()
      self.versionNum = versionNum

      GenericChunk.__init__(self, page, "BadVersionNumber",
"""<div id="wiki-message">
  <p><%= pageName %> has no version number <%=versionNum%>.</p>
</div>
""")


class LinkToExistingPageChunk(GenericChunk):

   def __init__(self, page, pageName, wikiRepository):
      self.pageName = pageName
      self.url = wikiRepository.makeUrl(self.pageName)

      GenericChunk.__init__(self, page, "LinkToExistingPage",
"""<a href="<%=url%>"><%=pageName%></a>""")


class SuccessfulSaveChunk(GenericChunk):

   def __init__(self, page, pageName, wikiRepository):
      self.pageName = pageName
      self.url = wikiRepository.makeUrl(self.pageName)

      GenericChunk.__init__(self, page, "SuccessfulSave",
"""<div id="wiki-message">
  <p>Your changes to <a href="<%= url %>"><%= pageName %></a> were
  saved successfully.</p>
</div>
""")


class CouldntSaveDueToConflictChunk(GenericChunk):

   def __init__(self, page, pageName, previousAuthor, wikiRepository):
      self.pageName = pageName
      self.url = wikiRepository.makeUrl(self.pageName)
      self.previousAuthor = previousAuthor

      GenericChunk.__init__(self, page, "CouldntSaveDueToConflict",
"""<p>User <%= previousAuthor %> saved a change to <a href="<%= url %>">
<%= pageName %></a> after you opened the page for editing.  The version
you tried to save is below.  To incorporate your changes into the page,
you might want to copy the text below into a text editor to save it,
then re-load the page into your browser and re-edit.</p>
""")

class VersionHistoryChunk(GenericChunk):

   def __init__(self, page, historyItems):
      self.historyItems = historyItems

      GenericChunk.__init__(self, page, "VersionHistory",
"""<div id="wiki-content">
  <h2>Page version history</h2>
  <table class="version-history">
    <thead>
    <tr>
      <td>Version</td>
      <td>Date</td>
      <td>Author</td>
      <td>Lines added/removed</td>
    </thead>
    <tbody>
    <%= historyItems %>
    </tbody>
  </table>
</div>
""")


class VersionHistoryItemChunk(GenericChunk):

   def __init__(self, page, versionNum, date, author, plusMinus):
      self.versionNum = versionNum
      self.date = friendlyDate(date)
      self.author = author
      self.plusMinus = plusMinus
      self.url = page.getPageUrl()

      GenericChunk.__init__(self, page, "VersionHistoryItem",
"""    <tr>
      <td class="col1"><a
      href="<%= url %>?version=<%= versionNum %>">v<%= versionNum %></a></td>
      <td class="col2"><%= date %></td>
      <td class="col3"><%= author %></td>
      <td class="col4"><%= plusMinus %></td>
    </tr>
""")

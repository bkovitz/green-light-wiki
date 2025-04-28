from teest import *
from StringIO import StringIO

from BodyExtractor import BodyExtractor

class ut_BodyExtractor:

   def testEverything(self):
      input = StringIO(
"""<HTML>
<HEAD>
   <TITLE>fake title here</TITLE>
</HEAD>
<BODY>
   Some body text begins here&#150;with an ampersand: &amp;.
   <P>
   Some more body <A HREF="http://nothing.com">text</A>.
</BODY>
</HTML>
"""
)

      expect = """
   Some body text begins here&#150;with an ampersand: &amp;.
   <P>
   Some more body <A HREF="http://nothing.com">text</A>.
"""

      extractor = BodyExtractor(input)

      TEST_EQ(expect, extractor.body())
      TEST_EQ("fake title here", extractor.title())


   def testLink(self):
      input = StringIO(
"""<HTML>
<HEAD>
   <TITLE>fake title here</TITLE>
   <LINK REL="STYLESHEET" HREF="http://glwiki.com/second-style.css" TYPE="text/css">
</HEAD>
<BODY>
   Some body text begins here&#150;with an ampersand: &amp;.
   <P>
   Some more body <A HREF="http://nothing.com">text</A>.
</BODY>
</HTML>
"""
)

      expect = [
         '<LINK REL="STYLESHEET" HREF="http://glwiki.com/second-style.css" TYPE="text/css">'
      ]

      extractor = BodyExtractor(input)

      TEST_EQ(expect, extractor.links())


   def testPhpOutput(self):
      input = StringIO(
"""Content-type: text/html
X-Powered-By: PHP/4.3.3
Set-Cookie: sbml_forums_fud_session_1063604505=419f87f7aa4b82faa989e935095a4551; expires=Fri, 03-Oct-2003 21:46:43 GMT; path=/forums/; domain=.sbml.org

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>SBML Discussion Lists: Welcome to the forum</title>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=ISO-8859-15">
<script language="javascript" src="lib.js" type="text/javascript"></script>
<link rel="StyleSheet" href="http://www.sbml.org/forums/theme/default/forum.css" type="text/css">
</head>
<body>
<p>fake text</p>
</body>
</html>
""")

      extractor = BodyExtractor(input)

      expectBody = "\n<p>fake text</P>\n"
      TEST_EQ(expectBody, extractor.body())

      expectLinks = [
         '<link rel="StyleSheet" href="http://www.sbml.org/forums/theme/default/forum.css" type="text/css">'
      ]
      TEST_EQ(expectLinks, extractor.links())

      expectCgiLeader = [
         "Content-type: text/html",
         "X-Powered-By: PHP/4.3.3",
         "Set-Cookie: sbml_forums_fud_session_1063604505=419f87f7aa4b82faa989e935095a4551; expires=Fri, 03-Oct-2003 21:46:43 GMT; path=/forums/; domain=.sbml.org"
      ]
      TEST_EQ(expectCgiLeader, extractor.cgiLeader())

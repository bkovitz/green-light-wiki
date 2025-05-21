expect = """Content-type: text/html
Set-Cookie: wiki-session={(20)}; Domain=.greenlightwiki.com; Max-Age=5184000; Path=/; Version=1;

<HTML><HEAD>
  <TITLE>edit Welcome Page</TITLE>
  <META NAME="keywords" CONTENT="wiki, green light wiki, unit test">
  <LINK REL="STYLESHEET" HREF="wiki.css" TYPE="text/css">
</HEAD>
<BODY><DIV ID="wiki-top">
  <P>&nbsp;</P>
  <P CLASS="title">edit Welcome Page</P>
</DIV>
<DIV ID="wiki-edit">
  <FORM ACTION="http://greenlightwiki.com/Welcome_Page" METHOD=POST><TEXTAREA ROWS=24 COLS=80 WRAP=VIRTUAL NAME="text">Describe Welcome Page here.</TEXTAREA>
<DIV ID="wiki-edit-buttons">
    <INPUT TYPE=SUBMIT VALUE=" Save "><INPUT TYPE=HIDDEN NAME="origVersion" VALUE="0">
  </DIV>
</FORM>
</DIV>
</BODY>
</HTML>
"""

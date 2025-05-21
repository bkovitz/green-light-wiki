from teest import *

from HtmlChunk import HtmlChunk, HtmlChunkFromFile

class ut_HtmlChunk:

   def testNoVariables(self):
      chunk = HtmlChunk("blah")
      TEST_EQ("blah", str(chunk))


   def testOneVariable(self):
      chunk = HtmlChunk('<P class="<%=classname%>">')
      chunk.classname = "blah"
      TEST_EQ('<P class="blah">', str(chunk))


   def testChunkFromFile(self):
      chunk = HtmlChunkFromFile(open("test-chunks.html", "r"), "SAMPLECHUNK")
      chunk.blah = "some text"
      TEST_EQ('<P>The expression some text goes here.</P>\n', str(chunk))


   def testChunkWithDefault(self):
      chunk = HtmlChunkFromFile(
         open("test-chunks.html", "r"),
         "NonexistentChunk",
         "default <%=blah%> text"
      )
      chunk.blah = "some text"
      TEST_EQ("default some text text", str(chunk))


   def testChunkWithObjectAsExpression(self):
      chunk = HtmlChunk("some <%=object%> goes here")
      chunk.object = HtmlChunk("thing")
      TEST_EQ("some thing goes here", str(chunk))


   def testNoneIsBlank(self):
      chunk = HtmlChunk(None)
      TEST_EQ("", str(chunk))


   def testConvertListToStrings(self):
      chunk = HtmlChunk(["a", "b", "c"])
      TEST_EQ("abc", str(chunk))


   def testNoneAsExpressionValueIsBlank(self):
      chunk = HtmlChunk("some <%=object%> goes here")
      chunk.object = None
      TEST_EQ("some  goes here", str(chunk))


   def testBackslashBeforeLessThan(self):
      chunk = HtmlChunk(r'<P class="\<%=classname%>">')
      chunk.classname = "blah"
      TEST_EQ('<P class="<%=classname%>">', str(chunk))


   def testBackslashBeforeN(self):
      chunk = HtmlChunk('First line \\nSecond line\\n')
      TEST_EQ("First line \nSecond line\n", str(chunk))


   def testEqualEqualInChunk(self):
      chunk = HtmlChunkFromFile(open("test-chunks.html", "r"), "ChunkWithDoubleEqual")
      TEST_EQ("Some text\n== Seemingly a chunk start\n", str(chunk))

class Indent:

   def __init__(self):
      self.level = 0


   def increment(self):
      self.level += 1


   def decrement(self):
      self.level -= 1


   def __str__(self):
      return self.render()

   
   def render(self, isBeginningOfLine=1):
      if isBeginningOfLine:
         return "  " * self.level
      else:
         return ""

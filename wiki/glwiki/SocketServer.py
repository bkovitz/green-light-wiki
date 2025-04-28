import socket, os
from threading import Thread
from io import StringIO
from Misc import forceRemove

from WikiClient import readAllFromSocket, socketTransaction


class KilledException:
   pass


class SocketServer:

   def __init__(self, address, service, timeout=None):
      self.address = address
      self.service = service
      self.timeout = timeout
      self.killed = False
      #os.umask(0002)
      os.umask(0o0002)
      self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
      if isinstance(self.address, str):
         forceRemove(self.address)
      self.sock.bind(self.address)
      self.sock.settimeout(self.timeout)
      self.listenThread = Thread(target=self.listen)
      self.listenThread.start()


   def listen(self):
      try:
         while 1:
            self.sock.listen(5)
            conn, addr = self._accept()
            data = readAllFromSocket(conn)
            command, environ, stdin = parseClientInput(data)

            if command == "test":
               conn.sendall("string from listener\n")
            elif command != "terminate":
               conn.sendall(self.service(environ, stdin))
            conn.shutdown(2)
            conn.close()

            if command == "terminate":
               break
      except KilledException:
         pass

      self.sock.shutdown(2)
      self.sock.close()


   def isAlive(self):
      return self.listenThread.isAlive()


   def terminate(self):
      socketTransaction(self.address, "terminate\n")


   def kill(self):
      self.killed = True


   def _accept(self):
      while 1:
         try:
            return self.sock.accept()
         except socket.timeout:
            if self.killed:
               raise KilledException()
            else:
               continue


# parser states

ST_IN_COMMAND = 0
ST_IN_ENVIRONMENT = 1
ST_IN_STDIN = 2

def parseClientInput(data):
   state = ST_IN_COMMAND
   command = ""
   environ = {}
   stdinString = ""
   for line in data.splitlines():
      if state == ST_IN_COMMAND:
         command = line
         state = ST_IN_ENVIRONMENT

      elif state == ST_IN_ENVIRONMENT:
         if not line:
            state = ST_IN_STDIN
         else:
            try:
               tag, value = line.split("=", 1)
               environ[tag] = value
            except ValueError:
               pass
      else:
         assert state == ST_IN_STDIN
         stdinString += line + "\n"

   return command, environ, StringIO(stdinString)

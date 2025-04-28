#! /home/bkovitz/software/bin/python

# This program can be run directly from Apache.  It needs no command-line
# arguments.  All parameters come from environment variables and stdin
# supplied by Apache.

# For efficiency, WikiClient.py imports nothing from any other .py file in
# glwiki.

import socket, os, sys
from traceback import print_exc


# for efficiency, the socket address is duplicated in Main.py
socketAddress = "wiki.socket"

import time

def main():
   f = open("dates", "a")
   #print >>f, time.strftime("%a %d-%b-%Y %H:%M:%S"), "WikiClient"
   print(time.strftime("%a %d-%b-%Y %H:%M:%S"), "WikiClient", file=f)
   f.flush()

   transactionString = makeTransactionString()
   try:
      wikiTransaction(transactionString)
   except socket.error:
      startServer()
      wikiTransaction(transactionString)


def startServer():
   os.system("./startwiki")


def wikiTransaction(transactionString):
   print(socketTransaction(socketAddress, transactionString))


def makeTransactionString():
   return (
      "wikipage\n"
      +
      envString(os.environ)
      +
      "\n\n"
      +
      sys.stdin.read()
   )


def socketTransaction(address, stringToSend):
   sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
   sock.connect(address)
   sock.sendall(stringToSend)
   sock.shutdown(1)  # inform server that we're done writing
   data = readAllFromSocket(sock)
   sock.close()
   return data


def envString(environ):
   return "\n".join([
      #"%s=%s" % item for item in environ.iteritems()
      "%s=%s" % item for item in environ.items()
   ])


def readAllFromSocket(sock):
   result = ""
   while 1:
      try:
         data = sock.recv(1024)
      except socket.error:
         break
      if not data or not len(data): break

      result += data

   return result


if __name__ == "__main__":
   try:
      main()
   except:
      print("Content-type: text/plain\n")
      print_exc(None, sys.stdout)


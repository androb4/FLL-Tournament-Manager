import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import thread
import time
import math

import display_audience

matchControlSocket = None

def countDownThread(threadName):
    for s in range(150, -1, -1):
        minutes = int(s/60)
        seconds = s - minutes*60
        timeString = str(minutes) + ":" + str(seconds).zfill(2)
        display_audience.displayAudienceWebsocket.write_message("timeString" + ";" + timeString)
        print timeString
        time.sleep(1)

class MatchControlWebsocketHandler(tornado.websocket.WebSocketHandler):
  def open(self):
      global matchControlSocket
      matchControlSocket = self
      print 'Match control connected'
      self.write_message("The server says: 'Hello'. Connection was accepted.")

  def on_message(self, message):
      if "start" in message:
          thread.start_new_thread(countDownThread, ("Thread-1", ) )

  def on_close(self):
      global matchControlSocket
      matchControlSocket = None
      print 'Match control disconnected'

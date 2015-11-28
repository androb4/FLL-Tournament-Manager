import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import thread
import time
import math
import json

import display_audience
import match_schedule

matchControlSocket = None

currentMatchIndex = 0

d = {
    'timerStart': 'false',
    'timeString': '2:30',
    'currentMatchIndex': 0,
    'matchList': match_schedule.matchList,
    'tableList': match_schedule.tableNames
}

print(json.dumps(d))

def countDownThread(threadName):
    d['timerStart'] = 'true'
    for s in range(150, -1, -1):
        minutes = int(s/60)
        seconds = s - minutes*60
        d['timeString'] = str(minutes) + ":" + str(seconds).zfill(2)
        if display_audience.displayAudienceWebsocket is not None:
            display_audience.displayAudienceWebsocket.write_message(json.dumps(d))
        if matchControlSocket is not None:
            matchControlSocket.write_message(json.dumps(d))
        print d['timeString']
        time.sleep(0.1)
    d['timerStart'] = 'false'
    if matchControlSocket is not None:
        matchControlSocket.write_message(json.dumps(d))

class MatchControlWebsocketHandler(tornado.websocket.WebSocketHandler):
  def open(self):
      global matchControlSocket
      matchControlSocket = self
      print 'Match control connected'
      if matchControlSocket is not None:
          matchControlSocket.write_message(json.dumps(d))

  def on_message(self, message):
      if "start" in message:
          thread.start_new_thread(countDownThread, ("Thread-1", ) )

  def on_close(self):
      global matchControlSocket
      matchControlSocket = None
      print 'Match control disconnected'

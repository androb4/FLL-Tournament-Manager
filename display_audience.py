import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import json

import match_control
import match_schedule

displayAudienceWebsocket = None

class DisplayAudienceWebsocketHandler(tornado.websocket.WebSocketHandler):
  def open(self):
      global displayAudienceWebsocket
      displayAudienceWebsocket = self
      print 'Audience display connected'
      self.write_message(json.dumps({'type':'matchList', 'data':{'matchIndex':match_schedule.currentMatchIndex, 'matchList':match_schedule.matchList}}))

  def on_message(self, message):
      print 'received:', message

  def on_close(self):
      global displayAudienceWebsocket
      displayAudienceWebsocket = None
      print 'Audience display disconnected'

def send(data):
    if displayAudienceWebsocket is not None:
        displayAudienceWebsocket.write_message(json.dumps(data))

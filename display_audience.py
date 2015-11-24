import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

import match_control

displayAudienceWebsocket = None

timerStart = False

class DisplayAudienceWebsocketHandler(tornado.websocket.WebSocketHandler):
  def open(self):
      global displayAudienceWebsocket
      displayAudienceWebsocket = self
      print 'Audience display connected'

  def on_message(self, message):
      print 'received:', message

  def on_close(self):
      global displayAudienceWebsocket
      displayAudienceWebsocket = None
      print 'Audience display disconnected'

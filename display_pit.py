import tornado
import json

import match_schedule

displayPitWebsocket = None


class DisplayPitWebsocketHandler(tornado.websocket.WebSocketHandler):
  def open(self):
      global displayPitWebsocket
      displayPitWebsocket = self
      self.write_message(json.dumps({'type':'matchList', 'data':{'matchList':match_schedule.matchList, 'tableList':match_schedule.tableNames, 'currentMatchIndex':match_schedule.currentMatchIndex}}))
      print 'Pit display connected'

  def on_message(self, message):
      print 'received:', message

  def on_close(self):
      global displayPitWebsocket
      displayPitWebsocket = None
      print 'Pit display disconnected'

def send(data):
    if displayPitWebsocket is not None:
        displayPitWebsocket.write_message(json.dumps(data))

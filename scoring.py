import tornado
import json

import match_schedule

scoringWebsocketHandler = None

class ScoringWebsocketHandler(tornado.websocket.WebSocketHandler):
  def open(self):
      global scoringWebsocketHandler
      scoringWebsocketHandler = self
      print 'Scoring connected'
      self.write_message(json.dumps({'type':'matchList', 'data':{'matchList':match_schedule.matchList, 'tableList':match_schedule.tableNames,}}))
      self.write_message(json.dumps({'type':'currentMatchIndex', 'data':{'currentMatchIndex':match_schedule.currentMatchIndex}}))
      self.write_message(json.dumps({'type':'scores', 'data':{}}))

  def on_message(self, message):
      print 'received:', message
      msg = json.loads(message)
      if msg['type'] == 'score':
          pass

  def on_close(self):
      global scoringWebsocketHandler
      scoringWebsocketHandler = None
      print 'Scoring disconnected'

def send(data):
    if scoringWebsocketHandler is not None:
        scoringWebsocketHandler.write_message(json.dumps(data))

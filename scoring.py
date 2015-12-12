import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import json

import match_schedule
import database
import rankings
import display_pit

scoringWebsocketHandler = None

class ScoringWebsocketHandler(tornado.websocket.WebSocketHandler):
  def open(self):
      global scoringWebsocketHandler
      scoringWebsocketHandler = self
      print 'Scoring connected'
      self.write_message(json.dumps({'type':'matchList', 'data':{'matchList':database.getMatchList(), 'tableList':database.getTableNames()}}))
      self.write_message(json.dumps({'type':'currentMatchIndex', 'data':{'currentMatchIndex':match_schedule.currentMatchIndex}}))
      self.write_message(json.dumps({'type':'scores', 'data':{}}))

  def on_message(self, message):
      print 'received:', message
      msg = json.loads(message)
      if msg['type'] == 'score':
          database.editScore(msg['data'])
          rankings.updateRankings()
          display_pit.send({'type':'rankings', 'data':{'rankings':database.getRankings()}})
          self.write_message(json.dumps({'type':'matchList', 'data':{'matchList':database.getMatchList(), 'tableList':database.getTableNames()}}))

  def on_close(self):
      global scoringWebsocketHandler
      scoringWebsocketHandler = None
      print 'Scoring disconnected'

def send(data):
    if scoringWebsocketHandler is not None:
        scoringWebsocketHandler.write_message(json.dumps(data))

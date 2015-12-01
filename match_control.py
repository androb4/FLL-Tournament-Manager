import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import threading
from time import sleep
import math
import json

import main_control_loop
import display_audience
import match_schedule

matchControlSocket = None

matchState = {
    'type': 'matchState',
    'timeString': '2:30',
    'timerStart': 'false',
    'matchReady': 'false'
}

websocketData = {
    'type': 'updateMatchList',
    'timerStart': 'false',
    'matchReady': 'true',
    'timeString': '2:30',
    'currentMatchIndex': 0,
    'matchList': match_schedule.matchList,
    'tableList': match_schedule.tableNames
}

class MatchControlWebsocketHandler(tornado.websocket.WebSocketHandler):
  def open(self):
      global matchControlSocket
      matchControlSocket = self
      print 'Match control connected'
      self.write_message(json.dumps({'type':'matchState', 'data':{'matchState':main_control_loop.matchState}}))
      self.write_message(json.dumps({'type':'matchList', 'data':{'matchList':match_schedule.matchList, 'currentMatchIndex':match_schedule.currentMatchIndex, 'tableList':match_schedule.tableNames}}))
      #self.write_message(json.dumps({'type':'matchList', 'data':{'matchList':match_schedule.matchList, 'tableList':match_schedule.tableNames, 'currentMatchIndex':websocketData['currentMatchIndex']}}))

  def on_message(self, message):
      print message
      msg = json.loads(message)
      if msg['type'] == 'matchStart':
          main_control_loop.matchState = main_control_loop.MatchState.START_MATCH
      if msg['type'] == 'resetTimer':
          if main_control_loop.matchState == main_control_loop.MatchState.DURING_MATCH:
              main_control_loop.matchState = main_control_loop.MatchState.POST_MATCH
          elif main_control_loop.matchState == main_control_loop.MatchState.POST_MATCH:
              main_control_loop.matchState = main_control_loop.MatchState.PRE_MATCH
      if msg['type'] == 'updateMatchIndex':
          match_schedule.currentMatchIndex = msg['data']['matchIndex']
      #websocketData.update(json.loads(message))
      #self.write_message(websocketData)

  def on_close(self):
      global matchControlSocket
      matchControlSocket = None
      print 'Match control disconnected'

def send(data):
    if matchControlSocket is not None:
        matchControlSocket.write_message(json.dumps(data))

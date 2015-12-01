import time
import threading
import json

import display_audience
import match_control
import match_schedule

matchState = 0
lastTime = 0
matchTime = 150


class MatchState:
    PRE_MATCH, START_MATCH, DURING_MATCH, END_MATCH, POST_MATCH = range(5)

class MainControlLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self.doStop = True
    def startTimer(self):
        self.doStop = False
    def stopTimer(self):
        self.doStop = True
    def stop(self):
        self.stopTimer()
        self._stopevent.set()
    def run(self):
        while not self._stopevent.is_set():
            global matchState
            global matchTime
            global lastTime
            time.sleep(0.1)
            if matchState == MatchState.PRE_MATCH:
                display_audience.send({'type':'currentMatch', 'data':{'matchIndex':match_schedule.currentMatchIndex, 'match':match_schedule.matchList}})
                matchTime = 150
                matchTimeString = str(int(matchTime/60)) + ":" + str(matchTime - int(matchTime/60)*60).zfill(2)
            if matchState == MatchState.START_MATCH:
                display_audience.send({'type':'playSound', 'data':{'playSound':'startMatch'}})
                startTime = time.time()
                matchState = MatchState.DURING_MATCH
            if matchState == MatchState.DURING_MATCH:
                matchTime = 150 - int(time.time() - startTime)
                matchTimeString = str(int(matchTime/60)) + ":" + str(matchTime - int(matchTime/60)*60).zfill(2)
                if lastTime != matchTime:
                    print matchTimeString
                if matchTime == 0:
                    matchState = MatchState.END_MATCH
                lastTime = matchTime
            if matchState == MatchState.END_MATCH:
                display_audience.send({'type':'playSound', 'data':{'playSound':'endMatch'}})
                match_schedule.currentMatchIndex =+ 1
                matchState = MatchState.POST_MATCH
            if matchState == MatchState.POST_MATCH:
                pass
            display_audience.send({'type':'matchTime', 'data':{'matchTimeString':matchTimeString}})
            display_audience.send({'type':'matchState', 'data':{'matchState':matchState}})
            match_control.send({'type':'matchTime', 'data':{'matchTimeString':matchTimeString}})
            match_control.send({'type':'matchState', 'data':{'matchState':matchState}})


            '''
            while t >= 0 and not self.doStop:
                #websocketData['timerStart'] = 'true'
                minutes = int(t/60)
                seconds = t - minutes*60
                timeString = str(minutes) + ':' + str(seconds).zfill(2)
                #matchState['timeString'] = str(minutes) + ':' + str(seconds).zfill(2)
                display_audience.send(json.dumps({'type':'matchTime', 'data':{'matchTime':timeString}}))
                match_control.send(json.dumps({'type':'matchTime', 'data':{'matchTime':timeString}}))
                print t
                t-=1
                time.sleep(0.1)
            if time == -1:
                global matchDone
                matchDone = True
                websocketData['timerStart'] = 'false'
                websocketData['matchReady'] = 'false'
                match_schedule.currentMatchIndex+=1
                matchControlSocket.write_message(json.dumps({'type':'matchIndex', 'data':{'currentMatchIndex':match_schedule.currentMatchIndex}}))
            self.stopTimer()
            #websocketData['timerStart'] = 'false'
            '''

import time
import threading

import display_audience
import match_control
import match_schedule
import database

matchTime = 0
matchState = 0
lastMatchState = 0
lastTime = 0
countFrom = 150

class MatchState:
    SETUP_MATCH, PRE_MATCH, START_MATCH, DURING_MATCH, END_MATCH, ABORT_MATCH, POST_MATCH = range(7)

class MainControlLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
    def stop(self):
        self._stopevent.set()
    def run(self):
        while not self._stopevent.is_set():
            global matchTime
            global matchState
            global lastMatchState
            global lastTime
            time.sleep(0.1)
            if matchState == MatchState.SETUP_MATCH:
                display_audience.send({'type':'matchList', 'data':{'matchIndex':match_schedule.currentMatchIndex, 'matchList':database.getMatchList()}})
                match_control.send({'type':'matchIndex', 'data':{'currentMatchIndex':match_schedule.currentMatchIndex}})
                matchState = MatchState.PRE_MATCH
            if matchState == MatchState.PRE_MATCH:
                matchTime = countFrom
                matchTimeString = str(int(matchTime/60)) + ":" + str(matchTime - int(matchTime/60)*60).zfill(2)
            if matchState == MatchState.START_MATCH:
                display_audience.send({'type':'playSound', 'data':{'playSound':'startMatch'}})
                startTime = time.time()
                matchState = MatchState.DURING_MATCH
            if matchState == MatchState.DURING_MATCH:
                matchTime = countFrom - int(time.time() - startTime)
                matchTimeString = str(int(matchTime/60)) + ":" + str(matchTime - int(matchTime/60)*60).zfill(2)
                if matchTime == 0:
                    matchState = MatchState.END_MATCH
            if matchState == MatchState.END_MATCH:
                display_audience.send({'type':'playSound', 'data':{'playSound':'endMatch'}})
                match_schedule.currentMatchIndex = match_schedule.currentMatchIndex + 1
                matchState = MatchState.POST_MATCH
            if matchState == MatchState.ABORT_MATCH:
                display_audience.send({'type':'playSound', 'data':{'playSound':'abortMatch'}})
                matchState = MatchState.POST_MATCH
            if matchState == MatchState.POST_MATCH:
                pass

            if lastMatchState != matchState:
                display_audience.send({'type':'matchState', 'data':{'matchState':matchState}})
                match_control.send({'type':'matchState', 'data':{'matchState':matchState}})
            if lastTime != matchTime:
                print matchTimeString
                display_audience.send({'type':'matchTime', 'data':{'matchTimeString':matchTimeString}})
                match_control.send({'type':'matchTime', 'data':{'matchTimeString':matchTimeString}})
            lastTime = matchTime
            lastMatchState = matchState

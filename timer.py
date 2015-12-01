from time import sleep
import math
import threading

timer = True

thread1 = None
matchDone = False

class countDownThread(threading.Thread):
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
            sleep(0.1)
            time = 150
            while time >= 0 and not self.doStop:
                #print time
                time-=1
                sleep(0.1)
            if time == -1:
                global matchDone
                matchDone = True
            print matchDone
            self.stopTimer()

try:
    thread1 = countDownThread()
    thread1.start()

    thread1.startTimer()

    sleep(500)
    thread1.stopTimer()

    thread1.stop()
except(KeyboardInterrupt, SystemExit):
    thread1.stop()
    raise

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

import main_control_loop
import event_setup
import match_control
import display_audience
import display_pit
import scoring
import database

application = tornado.web.Application([
  (r'/()', tornado.web.StaticFileHandler, {"path": "./static/index.html"}),
  (r'/match_control()', tornado.web.StaticFileHandler, {"path": "./static/match_control.html"}),
  (r'/match_control/websocket', match_control.MatchControlWebsocketHandler),
  (r'/display_audience()', tornado.web.StaticFileHandler, {"path": "./static/display_audience.html"}),
  (r'/display_audience/websocket', display_audience.DisplayAudienceWebsocketHandler),
  (r'/display_pit()', tornado.web.StaticFileHandler, {"path": "./static/display_pit.html"}),
  (r'/display_pit/websocket', display_pit.DisplayPitWebsocketHandler),
  (r'/scoring()', tornado.web.StaticFileHandler, {"path": "./static/scoring.html"}),
  (r'/scoring/websocket', scoring.ScoringWebsocketHandler),
  (r'/event_setup()', tornado.web.StaticFileHandler, {"path": "./static/event_setup.html"}),
  (r'/event_setup/websocket', event_setup.EventSetupWebsocketHandler),
  (r"/schedule_upload", event_setup.MatchListUploadHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./static"}),
])

if __name__ == "__main__":
    try:
        mainControlLoop = main_control_loop.MainControlLoop()
        mainControlLoop.start()
        application.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except(KeyboardInterrupt, SystemExit):
        mainControlLoop.stop()
        raise

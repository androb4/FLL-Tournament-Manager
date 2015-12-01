import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

import main_control_loop
import setup
import match_control
import display_audience
import display_pit


application = tornado.web.Application([
  (r'/()', tornado.web.StaticFileHandler, {"path": "./index.html"}),
  (r'/match_control()', tornado.web.StaticFileHandler, {"path": "./match_control.html"}),
  (r'/match_control/websocket', match_control.MatchControlWebsocketHandler),
  (r'/display_audience()', tornado.web.StaticFileHandler, {"path": "./display_audience.html"}),
  (r'/display_audience/websocket', display_audience.DisplayAudienceWebsocketHandler),
  (r'/display_pit()', tornado.web.StaticFileHandler, {"path": "./display_pit.html"}),
  (r'/display_pit/websocket', display_pit.DisplayPitWebsocketHandler),
  (r'/setup()', tornado.web.StaticFileHandler, {"path": "./setup.html"}),
  (r"/schedule_upload", setup.MatchListUploadHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
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

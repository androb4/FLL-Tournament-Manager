import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

import setup
import match_control
import display_audience

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write("yay")

application = tornado.web.Application([
  (r'/match_control()', tornado.web.StaticFileHandler, {"path": "./match_control.html"}),
  (r'/match_control/websocket', match_control.MatchControlWebsocketHandler),
  (r'/display_audience()', tornado.web.StaticFileHandler, {"path": "./display_audience.html"}),
  (r'/display_audience/websocket', display_audience.DisplayAudienceWebsocketHandler),
  (r'/setup()', tornado.web.StaticFileHandler, {"path": "./setup.html"}),
  (r"/schedule_upload", setup.MatchListUploadHandler),
  (r'/', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
])

if __name__ == "__main__":
  application.listen(9090)
  tornado.ioloop.IOLoop.instance().start()

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

import match_control
import display_audience

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write("yay")

application = tornado.web.Application([
  (r'/match_control/websocket', match_control.MatchControlWebsocketHandler),
  (r'/display_audience/websocket', display_audience.DisplayAudienceWebsocketHandler),
  (r'/', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
])

if __name__ == "__main__":
  application.listen(9090)
  tornado.ioloop.IOLoop.instance().start()

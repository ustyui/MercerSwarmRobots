"""Playing with tornado.websocket, to add markers to a Google Map using WebSockets
$ pip install tornado
$ python livemap.py --port=8888
Open http://localhost:8888 in one window
Each time http://localhost:8888/ping is opened in a second window, a
new marker is added to the map (at a random location)
Written with tornado==2.3
"""

import os
import json
import logging

import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import define, options


log = logging.getLogger(__name__)
WEBSOCKS = []


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/map.html")


class RandomLatLngSender(tornado.web.RequestHandler):
    """When an HTTP request is sent to /ping,
    this class sends a random lat/lng coord out
    over all websocket connections
    """

    def get(self):
        global WEBSOCKS
        log.debug("pinging: %r" % WEBSOCKS)

        import random
        # latlng = {#32.827695, -83.640428
        #     'lat': 32.827695
        #     'lng': -83.640428
        #     'title': "Thing!",
        # }
        latlng = {
            'lat': random.randint(30, 33),
            'lng': random.randint(-84, -82),
            'title': "Thing!",
        }   

        data = json.dumps(latlng)
        for sock in WEBSOCKS:
            sock.write_message(data)
        print(latlng)

class WebSocketBroadcaster(tornado.websocket.WebSocketHandler):
    """Keeps track of all websocket connections in
    the global WEBSOCKS variable.
    
    """
    def __init__(self, *args, **kwargs):
        super(EchoWebSocket, self).__init__(*args, **kwargs)

    def open(self):
        log.info("Opened socket %r" % self)
        print("Opened socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.append(self)

    def on_message(self, message):
        log.info(u"Got message from websocket: %s" % message)
        print("Got message from websocket: %s" % message)

    def on_close(self):
        log.info("Closed socket %r" % self)
        print("Closed socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.remove(self)

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)
        print("You said: "+message)

    def on_close(self):
        print("WebSocket closed")

settings = {
    # FIXME: Should really move maps.html into static/, and change the last
    # empty quotes to "static" (it's in same dir for gist)
    'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
}
print settings

application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/ping", RandomLatLngSender),
        (r"/sock", WebSocketBroadcaster),
        (r"/websocket", EchoWebSocket),
        ],
    **settings)


if __name__ == "__main__":
    define("port", default=8888, help="Run server on a specific port", type=int)
    tornado.options.parse_command_line()

    application.listen(options.port)
tornado.ioloop.IOLoop.instance().start()
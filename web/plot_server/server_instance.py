from bokeh.server.server import Server
from bokeh.command.util import build_single_handler_applications
import tornado.autoreload
import tornado.ioloop
import threading
import time


class BokehManager:
    """
    Trying to create class that can manage bokeh instance... I can call it
    outside of flask, but cant figure out how to access it from inside the app
    """
    def __init__(self, file):
        self.file = [file]
        self.argvs = {}
        self.urls = []
        self.host = 'localhost'
        self.bokeh_port = 6060

    def _run(self, bok_io_loop):
        apps = build_single_handler_applications(self.file, self.argvs)
        kwags = {
            'io_loop': bok_io_loop,
            'num_procs': 1,
            'sign_sessions': False,
            'port': self.bokeh_port,
            'allow_websocket_origin': ['127.0.0.1:8000']
        }
        srv = Server(apps,**kwags)

    def rest_of_tornado(self, io_loop_here):
        """test to see if I can shutdown while the server is running"""
        print('starting countdown')
        time.sleep(300)
        print('countdown finished')
        io_loop_here.stop()

    def start_bokeh(self):
        # initialize the tornado server
        io_loop = tornado.ioloop.IOLoop.instance()
        tornado.autoreload.start(io_loop)

        # call the turn off test
        nadostop = threading.Thread(target=self.rest_of_tornado,args=(io_loop,))
        nadostop.start()

        # add the io_loop to the bokeh server
        self._run(io_loop)
        print('starting the server')

        # run the bokeh server
        io_loop.start()


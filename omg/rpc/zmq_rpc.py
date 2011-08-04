import zmq
import json
import time
import traceback
import threading

from omg.rpc import Sender
from omg.rpc import Registry
from omg.rpc import Listener
from omg.log.api import debug

_ctx = None

def get_context():
    global _ctx
    if not _ctx:
        _ctx = zmq.Context()
    return _ctx
    

class ZMQListener(threading.Thread):
    def __init__(self, service, bind):
        super(ZMQListener, self).__init__()
        self.bind = bind
        self.service = service
        self.handlers = {}
        Registry()[service] = bind
        self.daemon = True
        self.shutdown = threading.Event()
        self.done = threading.Event()

    def _setup(self):
        self.ctx = get_context()
        self.sock = self.ctx.socket(zmq.REP)
        self.sock.bind(self.bind)

    def add_handler(self, request, callback):
        self.handlers[request] = callback

    def add_class(self, cls):
        debug("Registered API Class: %r" % cls)
        for m in dir(cls):
            a = getattr(cls, m)
            if callable(a):
                self.handlers[m] = a

    def shut(self, a, b):
        debug("Shutting down")
        self.shutdown.set()

    def is_shutdown(self):
        return self.done.is_set()

    def run(self):
        debug("Starting ZMQ Listener")
        self._setup()
        while not self.shutdown.is_set():
            resp = {}
            resp['exception'] = False
            try:
                msg = json.loads(self.sock.recv(flags=zmq.NOBLOCK))
            except zmq.ZMQError:
                time.sleep(0.001)
                continue
            debug("received: " + str(msg))
            if not self.handlers.has_key(msg['method']):
                debug("no handler for request type")
                resp['return'] = 'unknown method'
                resp['exception'] = True
            else:
                try:
                    resp['return'] = self.handlers[msg['method']](msg['args'])
                except Exception:
                    debug("unhandled exception while processing request")
                    resp['return'] = traceback.format_exc()
                    resp['exception'] = True
    
            resp['method'] = msg['method']
            
            self.sock.send(json.dumps(resp))
        self.done.set()

class ZMQSender(object):
    def __init__(self, service):
        self.connect = Registry()[service]
        self.ctx = get_context()
        self.sock = self.ctx.socket(zmq.REQ)
        self.sock.connect(self.connect)

    def call(self, method, args):
        msg = {}
        msg['method'] = method
        msg['args'] = args
        self.sock.send(json.dumps(msg))
        resp = json.loads(self.sock.recv())
        return resp


Listener.register(Listener, 'zmq', ZMQListener)
Sender.register(Sender, 'zmq', ZMQSender)


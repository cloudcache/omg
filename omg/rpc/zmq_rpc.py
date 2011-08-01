import zmq
import json
import traceback
import threading

from omg.rpc import Sender
from omg.rpc import Registry
from omg.rpc import Listener

class ZMQListener(threading.Thread):
    def __init__(self, service, bind):
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.REP)
        self.sock.bind(bind)
        self.service = service
        Registry()[service] = bind
        self.shutdown = False
        self.handlers = {}
        super(ZMQListener, self).__init__()

    def add_handler(self, request, callback):
        self.handlers[request] = callback

    def add_class(self, cls):
        for m in dir(cls):
            a = getattr(cls, m)
            if callable(a):
                self.handlers[m] = a

    def run(self):
        while not self.shutdown:
            resp = {}
            resp['exception'] = False
            try:
                msg = json.loads(self.sock.recv(flags=zmq.NOBLOCK))
            except zmq.ZMQError:
                continue
            print "received: ", msg
            if not self.handlers.has_key(msg['method']):
                print "no handler for request type"
                continue
            try:
                resp['return'] = self.handlers[msg['method']](msg['args'])
            except Exception:
                print "unhandled exception while processing request"
                resp['return'] = traceback.format_exc()
                resp['exception'] = True
    
            resp['method'] = msg['method']
            
            self.sock.send(json.dumps(resp))


class ZMQSender(object):
    def __init__(self, service):
        self.connect = Registry()[service]
        self.ctx = zmq.Context()
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


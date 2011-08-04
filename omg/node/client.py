from omg.config import Config
from omg.rpc import Sender
from omg.node import Node

class Client(object):
    def __init__(self, node):
        self.config = Config()
        self.node = Node(key=node)

    def connect(self):
        self.sender = Sender(self.node['uuid'])

    def call(self, method, args):
        return self.sender.call(method, args)


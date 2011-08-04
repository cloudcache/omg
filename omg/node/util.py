import os
import time
import socket

from omg.node import Nodes, Node

def register(rpc_uri):
    host = socket.gethostname()
    nodes = Nodes('all')
    if nodes.has_key(host):
        node = Node(key=nodes.item(host))
    else:
        node = Node()
        nodes[host] = node.key
        nodes.save()

    node['rpc_uri'] = rpc_uri
    node['hostname'] = host
    node['checkin'] = int(time.time())
    node.save()
    return node


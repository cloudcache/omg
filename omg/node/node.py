from omg.storable import Storable

class Node(Storable):
    '''
    'uuid':
        'state': <str>
        'checkin': <int>
        'rpc_uri': <str>
    '''
    def __init__(self, key=None, data=None):
        super(Node, self).__init__(key, data)
        self.data['uuid'] = self.key

Storable.storemap['Node'] = Node


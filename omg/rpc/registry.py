from omg.stateful import Stateful
from omg.storable import Storable

class Registry(Stateful, Storable):
    def __init__(self, scope=None):
        if not scope:
            scope = 'global'
        super(Registry, self).__init__(key=scope)

    def __setitem__(self, k, v):
        super(Registry, self).__setitem__(k, v)
        self.save()

Storable.storemap['Registry'] = Registry


from omg.stateful import Stateful
from omg.storable import Storable

class Config(Stateful, Storable):
    def __init__(self, scope=None):
        if not scope:
            scope = 'global'
        super(Config, self).__init__(key=scope)

    def incr(self, key):
        return self.store.incr(self.__class__.__name__, key)

Storable.storemap['Config'] = Config


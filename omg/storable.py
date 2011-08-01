from uuid import uuid4

from omg.store import Store

class Storable(object):
    storemap = {}

    def __init__(self, key=None, data=None, store=None):
        if not key:
            key = str(uuid4())
        self.key = key
        if not data:
            self.data = {}
        else:
            self.data = data
        self.store = store

    def _store(self):
        self.store = Store()

    def _load(self):
        self._store()
        self.store.load(self, self.key)
    
    def __getitem__(self, key):
        if not self.data:
            self._load()
        return self.data[key]

    def __setitem__(self, key, value):
        print key, value
        self.data[key] = value

    def __len__(self):
        if not self.data:
            self._load()
        return len(self.data)

    def __iter__(self):
        return self.data

    def save(self):
        if not self.store:
            self._store()
        self.store.obj(self)

    def items(self):
        if not self.data:
            self._load()
        return self.data.items()

    def __str__(self):
        if not self.data:
            self._load()
        return self.data.__str__()

    def __repr__(self):
        if not self.data:
            self._load()
        return self.data.__repr__()

    def remove(self, field):
        if not self.data:
            self._load()
        if self.data.has_key(field):
            return self.store.remove(self.__class__.__name__, self.key, field)

    def delete(self):
        if not self.data:
            self._load()
        self.store.delete(self.__class__.__name__, self.key)
        self.data = {}
        self.key = None


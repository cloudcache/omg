class Storable(object):
    def __init__(self, ns=None, key=None, store=None):
        self.ns = ns
        self.key = key
        self.store = store
        self.loaded = False
    
    def _load(self):
        pass

    def save(self):
        pass

class StoreScaler(Storable):
    def __init__(self, ns=None, key=None, store=None):
        super(StoreScaler, self).__init__(ns, key, store)
        self.data = None

namespace:key = value
namespace:key = {key: value, key, value}

class StoreHash(Storable):
    def __init__(self, ns=None, ey=None, store=None):
        super(StoreHash, self).__init__(ns, key, store)
        self.data = {}

    def __getitem__(self, key):
        if not self.loaded:
            self._load()
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __len__(self):
        return len(self.data)

    def __delitem__(self, key):
        pass

    def __contains__(self, item):
        return item in self.data


d = D()
d['a'] = 'b'

print d['a']
print d.data['a']

print d
print d.data


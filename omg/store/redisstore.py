import redis as _redis

from omg.defaults import Defaults
from omg.stateful import Stateful
from omg.store.connection import Store

class RedisStore(Stateful):
    def __init__(self, host=None):
        if not self._state():
            self.config = Defaults()
            if not host:
                host = self.config['store_host']
            self.r = _redis.Redis(host=host)

    def exists(self, klass, key, name):
        return self.r.hexists("%s:%s" % (klass, key), name)

    def load(self, obj, key):
        obj.data = self.r.hgetall("%s:%s" % (obj.__class__.__name__, key))

    def get(self, klass, key):
        d = self.r.hgetall("%s:%s" % (klass, key))
        return omg.storable.storemap[klass](key, d)

    def set(self, klass, key, val):
        self.r.set('%s:%s' % (klass, key), val)

    def incr(self, klass, key):
        return self.r.incr('%s:%s' % (klass, key))

    def obj(self, obj):
        key = "%s:%s" % (obj.__class__.__name__, obj.key)
        self.r.hmset(key, obj.data)
    
    def remove(self, klass, key, field):
        key = "%s:%s" % (klass, key)
        self.r.hdel(key, field)

    def delete(self, klass, key):
        key = "%s:%s" % (klass, key)
        self.r.delete(key) 

Store.register(Store, 'redis', RedisStore)


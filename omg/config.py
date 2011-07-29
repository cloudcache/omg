import omg
try:
    import json
except ImportError:
    import simplejson as json

class Config(omg.storable.Storable):
    '''
        This class is a bit of a special case when if comes to extending
        the Storable class. This is due to the fact that not only is 
        configuration data stored in the datastore but also in a confirguration
        file.
    '''
    __state = {}
    def __init__(self, path=None):
        if Config.__state:
            self.__dict__ = Config.__state
        else:
            if not path:
                path = '.'
            with open('%s/omg.conf' % path) as f:
                self.cdict = json.loads("".join(f.readlines()))
            Config.__state = self.__dict__
            super(Config, self).__init__('global')

    def __getitem__(self, key):
        if self.cdict.has_key(key):
            return self.cdict[key]
        return super(Config, self).__getitem__(key)

    def __setitem__(self, key, value):
        if self.cdict.has_key(key):
            self.cdict[key] = value
        super(Config, self).__setitem__(key, value)

    def incr(self, key):
        return self.store.incr(self.__class__.__name__, key)

omg.storable.storemap['Config'] = Config

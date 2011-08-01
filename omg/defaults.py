try:
    import json
except:
    import simplejson as json
import os

class Defaults(object):
    def __init__(self, path=None):
        if not path:
            if os.path.exists('./omg.conf'):
                path = '.'
            elif os.path.exists('../omg.conf'):
                path = '..'
        with open('%s/omg.conf' % path) as f:
            self.cdict = json.loads("".join(f.readlines()))

    def __getitem__(self, key):
        return self.cdict[key]

    def __setitem__(self, key, value):
        self.cdict[key] = value

    def has_key(self, key):
        return self.cdict.has_key(key)

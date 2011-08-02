from omg.defaults import Defaults

class Factory(object):
    classmap = {}
    configname = None
    configsource = None

    def __new__(cls, *args, **kwargs):
        m = cls.classmap
        n = cls.configname
        if not cls.configsource:
            cls.configsource = Defaults()
        conf = cls.configsource
        try:
            return m[cls][conf[n]](*args, **kwargs)
        except:
            raise

    @classmethod
    def register(cls, k, t, c):
        if not cls.classmap.has_key(k):
            cls.classmap[k] = {}
        cls.classmap[k][t] = c

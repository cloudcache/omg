import omg

active_store = None

class Store(object):
    storemap = {}

    def __new__(cls, *args, **kwargs):
        sm = Store.storemap
        conf = omg.config.Config()
        return sm[conf['store_type']](*args, **kwargs) 


__all__ = ['store', 'redisstore']


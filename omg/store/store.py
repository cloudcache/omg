import omg

class Store(object):
    storemap = {}
    def __new__(cls, **kwargs):
        sm = Store.sm
        conf = omg.config.Config()
        return sm[conf['store_type'].__new__(sm[conf['store_type'], 
            **kwargs) 

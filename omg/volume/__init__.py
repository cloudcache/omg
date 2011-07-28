import omg

class Volume(object):
    volumemap = {}

    def __new__(cls, *args, **kwargs):
        vm = Volume.volumemap
        conf = omg.config.Config()
        return vm[conf['volume_type']](*args, **kwargs)



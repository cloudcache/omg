from omg.storable import Storable

class Volume(Storable):
    '''
    '<uuid>': {
        'format': <str>
        'mounted': <bool>
        'device': <str>
    }
    '''

    def __init__(self, key=None):
        super(Volume, self).__init__(key)

    def mount():
        pass

    def umount():
        pass


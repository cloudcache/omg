from omg.storable import Storable

class Images(Storable):
    '''
    'base':
        'name': <uuid>
    '''

    def list(self):
        return self.data

    def add(self, name, vol):
        self.data[name] = vol.key

    def rem(self, name):
        pass

Storable.storemap['Images'] = Images

import omg

class Images(omg.storable.Storable):
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

omg.storable.storemap['Images'] = Images

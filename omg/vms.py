import omg

class Vms(omg.storable.Storable):
    '''
    'base':
        'name': <uuid>
    '''

    def list(self):
        return self.data

    def add(self, name, vm):
        self.data[name] = vm.key

    def rem(self, name):
        pass

omg.storable.storemap['Vms'] = Vms

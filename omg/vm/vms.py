from omg.storable import Storable

class Vms(Storable):
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

Storable.storemap['Vms'] = Vms

from omg.storable import Storable

class Nodes(Storable):
    def list(self):
        return self.data

    def add(self, uuid, node):
        self.data[uuid] = node.key

    def rem(self, uuid):
        pass

Storable.storemap['Nodes'] = Nodes

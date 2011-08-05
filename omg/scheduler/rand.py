from omg.scheduler.factory import Scheduler
from omg.stateful import Stateful
from omg.node import Nodes

class RandomScheduler(Stateful):
    def get_node(self, node):
        ''' Simply returns a random node from the database. '''
        nodes = Nodes()
        return nodes.ramdom()

Scheduler.register(Scheduler, 'random', RandomScheduler)


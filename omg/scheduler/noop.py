from omg.scheduler.factory import Scheduler
from omg.stateful import Stateful
from omg.node import Nodes

class NoopScheduler(Stateful):
    def get_node(self, node):
        ''' Simply returns the first node in the database '''
        nodes = Nodes()
        for k, v in nodes.items():
            return v

Scheduler.register(Scheduler, 'noop', NoopScheduler)


from omg.log.api import debug
from omg.config import Config
from omg.rpc import Sender
from omg.vm import VM, Vms
from omg.node import Node, Nodes

class Api(object):
    def __init__(self):
        self.config = Config()

    def ping(self, msg):
        return msg

    def vm_list(self, args):
        ret = []
        vms = Vms(args)
        for _, val in vms.items():
            vm = VM(val)
            vm._load()
            vm['uuid'] = vm.key
            if vm['ip'] == 'None':
                vm['ip'] = 'DHCP'
            ret.append(vm.data)
        return ret

    def vm_get(self, args):
        vm = VM(key=args['name'])
        vm._load()
        return vm.data

    def vm_edit(self, args):
        vm = VM(key=args['name'])
        vm._load()
        vm[args['key']] = args['value']
        vm.save()
        vm.update_xml()
        return vm[args['key']]

    def vm_create(self, args):
        vm = VM()
        top_half = vm.create_db(name=args['name'], ram=args['ram'], cpus=args['cpus'],
            base=args['base'])
        if not top_half:
            return False
        debug(vm['node'])
        bottom_half = Sender(vm['node']).call('vm_create', {'uuid': vm['uuid']})
        return [top_half, bottom_half]

    def vm_start(self, args):
        vm = VM(key=args['name'])
        return Sender(vm['node']).call('vm_start', {'uuid': vm['uuid']})

    def vm_stop(self, args):
        vm = VM(key=args['name'])
        return Sender(vm['node']).call('vm_stop', {'uuid': vm['uuid']})

    def vm_destroy(self, args):
        vm = VM(key=args['name'])
        return Sender(vm['node']).call('vm_destroy', {'uuid': vm['uuid']})
        return vm.destroy()

    def vm_restart(self, args):
        vm = VM(key=args['name'])
        return Sender(vm['node']).call('vm_restart', {'uuid': vm['uuid']})
        return vm.restart()

    def vm_delete(self, args):
        vm = VM(key=args['name'])
        return Sender(vm['node']).call('vm_delete', {'uuid': vm['uuid']})

    def config_set(self, args):
        self.config[args['key']] = args['value']
        self.config.save()
        return self.config[args['key']]

    def config_get(self, args):
        key = args['key']
        if key:
            return {key: self.config[key]}
        self.config._load()
        return self.config.data

    def node_list(self, args):
        ret = []
        nodes = Nodes('all')
        for _, val in nodes.items():
            node = Node(val)
            node._load()
            ret.append(node.data)
        return ret

    def node_get(self, args):
        node= Node(key=args['name'])
        node._load()
        return node.data

    def node_deactivate(self, args):
        return self.ping(args)

    def node_activate(self, args):
        return self.ping(args)

    def node_register(self, args):
        return self.ping(args)


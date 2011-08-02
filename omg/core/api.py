from omg.vm import VM
from omg.vm import Vms
from omg.log import Log
from omg.config import Config

class Api(object):
    def __init__(self):
        self.config = Config()
        self.log = Log()

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
        return vm.create(name=args['name'], ram=args['ram'], cpus=args['cpus'],
            base=args['base'])

    def vm_start(self, args):
        vm = VM(key=args['name'])
        return vm.start()

    def vm_stop(self, args):
        vm = VM(key=args['name'])
        return vm.stop()

    def vm_destroy(self, args):
        vm = VM(key=args['name'])
        return vm.destroy()

    def vm_restart(self, args):
        vm = VM(key=args['name'])
        return vm.restart()

    def vm_delete(self, args):
        vm = VM(key=args['name'])
        return vm.delete()

    def config_set(self, args):
        self.config[args['key']] = args['value']
        return self.config[args['key']]

    def config_get(self, args):
        key = args['key']
        if key:
            return {key: self.config[key]}
        self.config._load()
        return self.config.data

    def node_list(self, args):
        return self.ping(args)

    def node_get(self, args):
        return self.ping(args)

    def node_deactivate(self, args):
        return self.ping(args)

    def node_activate(self, args):
        return self.ping(args)



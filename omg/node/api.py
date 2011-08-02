from omg.vm import VM
from omg.vm import Vms

class Api(object):
    def ping(self, msg):
        return msg.upper()

    def list(self, msg):
        ret = []
        vms = Vms(msg)
        for _, val in vms.items():
            vm = VM(val)
            vm._load()
            vm['uuid'] = vm.key
            if vm['ip'] == 'None':
                vm['ip'] = 'DHCP'
            ret.append(vm.data)
        return ret


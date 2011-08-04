import psutil

from omg.vm import VM
from omg.vm import Vms

class Api(object):
    def ping(self, msg):
        return msg.upper()

    def node_resources(self, msg):
        meminfo = [psutil.TOTAL_PHYMEM, psutil.avail_phymem()]
        return meminfo

    def vm_list(self, msg):
        return self.ping(msg)

    def vm_create(self, msg):
        vm = VM(key=msg['uuid'])
        return vm.create()

    def vm_delete(self, msg):
        vm = VM(key=msg['uuid'])
        return vm.delete()

    def vm_start(self, msg):
        vm = VM(key=msg['uuid'])
        return vm.start()

    def vm_stop(self, msg):
        vm = VM(key=msg['uuid'])
        return vm.stop()

    def vm_destroy(self, msg):
        vm = VM(key=msg['uuid'])
        return vm.destroy()

        

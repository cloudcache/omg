import libvirt

from omg.config import Config
from omg.log import Log

class Hypervisor(object):
    def __init__(self):
        self.conf = Config()
        self.log = Log()
        self.conn = libvirt.open(self.conf['hypervisor_uri'])

    def define(self, xml):
        self.conn.defineXML(xml)

    def start(self, vm):
        self.log.debug("starting %s" % vm.key)
        try:
            dom = self.conn.lookupByUUIDString(vm.key)
        except:
            self.define(vm.xml())
            dom = self.conn.lookupByUUIDString(vm.key)
        dom.create()

    def stop(self, uuid):
        self.log.debug("stopping %s" % uuid)
        dom = self.conn.lookupByUUIDString(uuid)
        dom.shutdown()
    
    def destroy(self, uuid):
        self.log.debug("destroying %s" % uuid)
        dom = self.conn.lookupByUUIDString(uuid)
        try:
            dom.destroy()
        except:
            pass

    def undefine(self, uuid):
        self.log.debug("undefining %s" % uuid)
        try:
            self.destroy(uuid)
        except libvirt.libvirtError:
            pass
        dom = self.conn.lookupByUUIDString(uuid)
        dom.undefine()

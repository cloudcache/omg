import libvirt
import omg

class Hypervisor(object):
    def __init__(self):
        self.conf = omg.config.Config()
        self.conn = libvirt.open(self.conf['hypervisor_uri'])

    def define(self, xml):
        self.conn.defineXML(xml)

    def start(self, uuid):
        print "starting %s" % uuid
        dom = self.conn.lookupByUUIDString(uuid)
        dom.create()

    def stop(self, uuid):
        print "stopping %s" % uuid
        dom = self.conn.lookupByUUIDString(uuid)
        dom.shutdown()
    
    def destroy(self, uuid):
        print "destroying %s" % uuid
        dom = self.conn.lookupByUUIDString(uuid)
        dom.destroy()

    def undefine(self, uuid):
        print "undefining %s" % uuid
        try:
            self.destroy(uuid)
        except libvirt.libvirtError:
            pass
        dom = self.conn.lookupByUUIDString(uuid)
        dom.undefine()

import os
import subprocess

import omg

DOMAIN_TPL = '''<domain type='kvm'>
  <name>%(name)s</name>
  <uuid>%(key)s</uuid>
  <memory>%(ram)s</memory>
  <currentMemory>%(ram)s</currentMemory>
  <vcpu>%(cpus)s</vcpu>
  <os>
    <type>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/bin/kvm</emulator>
    <disk type='block' device='disk'>
      <source dev='%(path)s/%(image)s.img'/>
      <target dev='hda' bus='virtio'/>
      <driver name='qemu' type='qcow2'/>
    </disk>
    <interface type='bridge'>
      <mac address='%(mac)s'/>
      <source bridge='br0'/>
    </interface>
    <input type='tablet' bus='usb'/> 
    <input type='mouse' bus='ps2'/>
    <graphics type='vnc' port='%(vnc)s' listen='0.0.0.0'/>
  </devices>
</domain>'''

class VM(omg.storable.Storable):
    '''
    'name':
        'image': <uuid>
        'base': <uuid>
        'cpus': <int>
        'ram': <int>
        'ip': <str>
        'mac': <str>
        'vnc': <int>
    '''
    def __init__(self, key=None, data=None):
        super(VM, self).__init__(key, data)
        self.conf = omg.config.Config()
        self.hv = omg.hypervisor.Hypervisor()

    def create(self, base=None, cpus=None, ram=None, name=None, ip=None, 
        mac=None, vnc=None):
        store = omg.store.Store()

        if not name:
            print "Missing name"
            return 
        if store.exists("Vms", "active", name):
            print "VM Already Exists"
            return

        # set defaults
        if not base:
            base = self.conf['vm_default_base']
        if not cpus:
            cpus = self.conf['vm_default_cpus']
        if not ram:
            ram = self.conf['vm_default_ram']
        if not vnc:
            vnc = self.conf.incr('vnc')
        if not mac:
            mac = omg.util.uniq_mac()

        images = omg.images.Images('base')
        self.data['base'] = images[base]
        self.data['cpus'] = cpus
        self.data['ram'] = ram
        self.data['ip'] = ip
        self.data['mac'] = mac
        self.data['vnc'] = vnc
        self.data['state'] = 'off'
        self.data['name'] = name

        img = omg.volume.Volume()
        img.create(self.data['base'])
   
        self.data['image'] = img.key
       
        print self.data

        t = {}
        t.update(self.data)
        t['key'] = self.key
        t['path'] = self.conf['image_path']
        domain = DOMAIN_TPL % t
        print domain 

        xmld = "%s/%s.xml" % (self.conf['domain_xml_path'], self.key)
        with open(xmld, 'w') as fp:
            fp.write(domain)
            os.chmod(xmld, 0744)
        print self.data
        
        vms = omg.vms.Vms('active')
        vms[self.data['name']] = self.key
        self.hv.define(domain)

        self.save()
        img.save()
        vms.save()

    def start(self):
        self.hv.start(self.key)   

    def stop(self):
        self.hv.stop(self.key)   
     
    def destroy(self):
        self.hv.destroy(self.key)

    def delete(self):
        self._load()
        try:
            self.hv.undefine(self.key)
            xmld = "%s/%s.xml" % (self.conf['domain_xml_path'], self.key)
            os.unlink(xmld)
        except:
            pass
        vms = omg.vms.Vms('active')
        print self.key
        print self.data
        vms.remove(self.data['name'])
        img = omg.volume.Volume(self.data['image'])
        img.delete()
        super(VM, self).delete()


omg.storable.storemap['VM'] = VM


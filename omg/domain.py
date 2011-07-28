DOMAIN_TPL = '''<domain type='kvm'>
  <name>%(name)s</name>
  <uuid>%(key)s</uuid>
  <memory>%(ram)d</memory>
  <currentMemory>%(ram)d</currentMemory>
  <vcpu>%(cpus)d</vcpu>
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
      <source dev='%(image)s'/>
      <target dev='hda' bus='ide'/>
    </disk>
    <interface type='bridge'>
      <mac address='%(mac)s'/>
      <source bridge='br0'/>
    </interface>
    <input type='tablet' bus='usb'/> 
    <input type='mouse' bus='ps2'/>
    <graphics type='vnc' port='%(vnc)' listen='0.0.0.0'/>
  </devices>
</domain>'''

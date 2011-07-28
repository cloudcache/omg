#!/usr/bin/env python
import sys
import os
import subprocess
import redis
from copy import deepcopy
from uuid import uuid4

import omg

def main(argv):
    store = omg.store.Store()
    config = omg.config.Config()

    if argv[0] == 'base-create':
        img = omg.volume.Volume()
        img['name'] = argv[1]

        if store.exists("Images", "base", img['name']):
            print "base image already exists"
            return

        img.save()
        print "base uuid: %s" % img.key
        print img
        print img.key
        base = Images('base')
        base[img['name']] = img.key
        base.save()
    elif argv[0] == 'base-list':
        imgs = omg.images.Images('base')
        print imgs

    elif argv[0] == 'vm-list':
        tpl = "{name:20}{uuid:40}{cpus:6}{ram:5}{vnc:8}{state:7}{ip:5}"
        vms = omg.vms.Vms('active')
        print tpl.format(name="NAME", uuid="UUID", cpus="CPUS", ram="RAM",
            vnc="VNC", state="STATE", ip="IP")
        for k,v in vms.items():
            t = {}
            vm = omg.vm.VM(v)
            vm._load()
            t['uuid'] = vm.key
            t.update(vm.data)
            t['vnc'] = ":%d" % (5900+int(t['vnc']))
            if t['ip'] == 'None':
                t['ip'] = 'DHCP'
            print tpl.format(**t)
    elif argv[0] == 'vm-start':
        vm = omg.vm.VM(key=argv[1])
        print vm.start()
    elif argv[0] == 'vm-restart':
        vm = omg.vm.VM(key=argv[1])
        print vm.stop()
        print vm.start()
    elif argv[0] == 'vm-stop':
        vm = omg.vm.VM(key=argv[1])
        print vm.stop()
    elif argv[0] == 'vm-destroy':
        vm = omg.vm.VM(key=argv[1])
        print vm.destroy()
    elif argv[0] == 'vm-delete':
        vm = omg.vm.VM(key=argv[1])
        print vm.delete()
    elif argv[0] == 'vm-create':
        vm = omg.vm.VM()
        vm.create(name=argv[1])

    elif argv[0] == 'conf-set':
        config[argv[1]] = argv[2]
        config.save()
        print config[argv[1]]
    elif argv[0] == 'conf-get':
        print config

    else:
        print "unknown/missing command"

if __name__ == '__main__':
    main(sys.argv[1:])


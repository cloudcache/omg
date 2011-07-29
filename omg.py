#!/usr/bin/env python
import sys
import redis
import shutil
import os.path
import inspect

BINPATH = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.insert(0, BINPATH)

import omg

class Command(object):
    def __init__(self):
        self.config = omg.config.Config(BINPATH)
        self.store = omg.store.Store()

    @classmethod
    def help(cls):
        l = get_commands(cls)
        for i in l:
            args = "> <".join(get_args(getattr(cls, i)))
            if args:
                args = "<%s>" % args
            print >> sys.stderr, '\t%s %s %s' % (cls.__name__.lower(), i, args)


class Base(Command):
    def create(self, name, path):
        img = omg.volume.Volume()
        img['name'] = name

        if self.store.exists("Images", "base", img['name']):
            print "base image already exists"
            return

        img.save()
        print "base uuid: %s" % img.key
        print img
        print img.key
        base = omg.images.Images('base')
        base[img['name']] = img.key
        base.save()
        shutil.copy(path, "%s/%s.img" % (self.config['base_path'], img.key))

    def list(self):
        imgs = omg.images.Images('base')
        print imgs

    def delete(self, name):
        print "name: ", name


class Image(Command):
    pass


class Vm(Command):
    def list(self):
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

    def create(self, name):
        vm = omg.vm.VM()
        vm.create(name=name)

    def restart(self, name):
        vm = omg.vm.VM(key=name)
        print vm.stop()
        print vm.start()

    def start(self, name):
        vm = omg.vm.VM(key=name)
        print vm.start()

    def stop(self, name):
        vm = omg.vm.VM(key=name)
        print vm.stop()

    def destroy(self, name):
        vm = omg.vm.VM(key=name)
        print vm.destroy()

    def delete(self, name):
        vm = omg.vm.VM(key=name)
        print vm.delete()


class Config(Command):
    def set(self, key, value):
        self.config[key] = value
        self.config.save()
        print self.config[key]

    def get(self):
        print self.config


class Help(Command):
    @classmethod
    def help(cls):
        print >> sys.stderr, '\thelp'
        for k,v in COMMAND_MAP.items():
            if k != 'help':
                v.help()


COMMAND_MAP = {
    'base': Base,
    'image': Image,
    'vm': Vm,
    'config': Config,
    'help': Help
}

def arg_count(fn):
    t = inspect.getargspec(fn)
    return len(t.args)-1

def get_args(fn):
    t = inspect.getargspec(fn)
    return t.args[1:]

def get_commands(kls):
    return [x for x in dir(kls) if x[0] != '_' and callable(getattr(kls,x))]

def help(msg, kls):
    print >> sys.stderr, "ERROR:", msg
    kls.help()
    sys.exit(1)

def main(argv):
    if len(argv) < 1:
        help("Missing Command", Help)

    cmd = argv.pop(0)

    try:
        command = COMMAND_MAP[cmd]()
    except KeyError:
        help("Unknown Command", Help)

    try:
        try:
            sub = argv.pop(0)
        except IndexError:
            help("Missing Action", command)
        fn = getattr(command, sub)
        c = len(argv)
        a = arg_count(fn)
        if c != a:
            msg = "Not enough" if c < a else "Too many"
            msg +="Arguments"
            help(msg, command)
        fn(*argv)
    except AttributeError:
        help("Unknown Action", Help)

if __name__ == '__main__':
    main(sys.argv[1:])


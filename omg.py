#!/usr/bin/env python
''' Frontend tool for omg '''

# shut up pylint
#pylint: disable=R0201
#pylint: disable=C0103

import sys
import redis
import shutil
import os.path
import inspect

BINPATH = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.insert(0, BINPATH)

import omg

class Command(object):
    ''' Command parent class '''
    def __init__(self):
        self.config = omg.config.Config(BINPATH)
        self.store = omg.store.Store()

    @classmethod
    def help(cls):
        ''' Display help. '''
        cmds = get_commands(cls)
        name = cls.__name__.lower()
        for cmd in cmds:
            func = getattr(cls, cmd)
            args = "> <".join(get_args(func))
            if args:
                args = "<%s>" % args
            if name == 'help':
                cmds = ''
            opt = ''
            for l in reversed(get_optional(func)):
                    opt = '[<%s> %s]' % (l, opt)
            print >> sys.stderr, '    %s %s %s %s' % (name, cmd, args, opt)
            print >> sys.stderr, '        ', func.__doc__.strip()


class Base(Command):
    ''' Base image manager '''
    def create(self, name, path):
        ''' Create base image. '''
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
        ''' List existing images. '''
        imgs = omg.images.Images('base')
        print imgs

    def delete(self, name):
        ''' Delete a base image. '''
        print "name: ", name


class Image(Command):
    ''' Image manager '''
    pass


class Vm(Command):
    ''' Vm manager '''
    def list(self):
        ''' List current vms. '''
        tpl = "{name:20}{uuid:40}{cpus:6}{ram:5}{vnc:8}{state:7}{ip:5}"
        vms = omg.vms.Vms('active')
        print tpl.format(name="NAME", uuid="UUID", cpus="CPUS", ram="RAM",
            vnc="VNC", state="STATE", ip="IP")
        for _, val in vms.items():
            temp = {}
            vm = omg.vm.VM(val)
            vm._load()
            temp['uuid'] = vm.key
            temp.update(vm.data)
            temp['vnc'] = ":%d" % (5900+int(temp['vnc']))
            if temp['ip'] == 'None':
                temp['ip'] = 'DHCP'
            print tpl.format(**temp)

    def create(self, name, ram=None, cpus=None, base=None):
        ''' Create a new vm. '''
        vm = omg.vm.VM()
        vm.create(name=name, ram=ram, cpus=cpus, base=base)

    def restart(self, name):
        ''' Restart a vm. '''
        vm = omg.vm.VM(key=name)
        print vm.stop()
        print vm.start()

    def start(self, name):
        ''' Start a vm. '''
        vm = omg.vm.VM(key=name)
        print vm.start()

    def stop(self, name):
        ''' Stop a vm. '''
        vm = omg.vm.VM(key=name)
        print vm.stop()

    def destroy(self, name):
        ''' Destroy a vm. '''
        vm = omg.vm.VM(key=name)
        print vm.destroy()

    def delete(self, name):
        ''' Delete a vm. '''
        vm = omg.vm.VM(key=name)
        print vm.delete()


class Config(Command):
    ''' Config Manager '''
    def set(self, key, value):
        ''' Set a configuration value. '''
        self.config[key] = value
        self.config.save()
        print self.config[key]

    def get(self):
        ''' Get configuration values. '''
        print self.config


class Help(Command):
    ''' Help Manager '''
    @classmethod
    def help(cls):
        ''' This help '''
        super(Help, cls).help()
        for key, val in COMMAND_MAP.items():
            if key != 'help':
                val.help()


COMMAND_MAP = {
    'base': Base,
    'image': Image,
    'vm': Vm,
    'config': Config,
    'help': Help
}

def arg_count(func):
    ''' Get number of arguments for a function '''
    temp = inspect.getargspec(func)
    amax = len(temp.args) - 1
    amin = amax-len(temp.defaults) if temp.defaults else amax
    return (amin, amax)

def get_args(func):
    ''' Get argument names '''
    temp = inspect.getargspec(func)
    optc = len(temp.defaults) if temp.defaults else 0
    return temp.args[1:-optc]

def get_optional(func):
    ''' Get optional arguments '''
    temp = inspect.getargspec(func)
    if temp.defaults:
        return temp.args[-len(temp.defaults):]
    else:
        return [] 

def get_commands(kls):
    ''' Get class function names '''
    return [x for x in dir(kls) if x[0] != '_' and callable(getattr(kls, x))]

def help(msg, kls, ret=1):
    ''' Print help message '''
    print >> sys.stderr, msg
    kls.help()
    sys.exit(ret)

def main(argv):
    ''' Program entry point '''
    if len(argv) < 1:
        help("Missing Command", Help)

    cmd = argv.pop(0)

    if cmd == 'help':
        help("Help", Help, 0)

    try:
        command = COMMAND_MAP[cmd]()
    except KeyError:
        help("Unknown Command", Help)

    try:
        try:
            sub = argv.pop(0)
        except IndexError:
            help("Missing Action", command)
        func = getattr(command, sub)
        count = len(argv)
        amin, amax = arg_count(func)
        if amin <= count <= amax:
            func(*argv)
        else:
            msg = "Not enough" if count < amin else "Too many"
            msg +=" Arguments"
            help(msg, command)
    except AttributeError:
        help("Unknown Action", Help)

if __name__ == '__main__':
    main(sys.argv[1:])


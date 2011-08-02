#!/usr/bin/env python
''' Frontend tool for omg '''

# shut up pylint
#pylint: disable=R0201
#pylint: disable=C0103

import os
import sys
import redis
import shutil
import os.path
import inspect
import traceback

BINPATH = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.insert(0, BINPATH)
DEBUG = os.environ.has_key('DEBUG')

from omg.config import Config
from omg.store import Store
from omg.vm import VM
from omg.vm import Vms
from omg.volume import Volume
from omg.image import Images

class Command(object):
    ''' Command parent class '''
    def __init__(self):
        self.config = Config()
        self.store = Store()

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
        img = Volume()
        img['name'] = name

        if self.store.exists("Images", "base", img['name']):
            print "base image already exists"
            return

        img.save()
        print "base uuid: %s" % img.key
        print img
        print img.key
        base = Images('base')
        base[img['name']] = img.key
        base.save()
        shutil.copy(path, "%s/%s.img" % (self.config['base_path'], img.key))

    def list(self):
        ''' List existing images. '''
        imgs = Images('base')
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
        vms = Vms('active')
        print tpl.format(name="NAME", uuid="UUID", cpus="CPUS", ram="RAM",
            vnc="VNC", state="STATE", ip="IP")
        for _, val in vms.items():
            temp = {}
            vm = VM(val)
            vm._load()
            temp['uuid'] = vm.key
            temp.update(vm.data)
            temp['vnc'] = ":%d" % (5900+int(temp['vnc']))
            if temp['ip'] == 'None':
                temp['ip'] = 'DHCP'
            print tpl.format(**temp)

    def create(self, name, ram=None, cpus=None, base=None):
        ''' Create a new vm. '''
        vm = VM()
        vm.create(name=name, ram=ram, cpus=cpus, base=base)

    def restart(self, name):
        ''' Restart a vm. '''
        vm = VM(key=name)
        print vm.stop()
        print vm.start()

    def start(self, name):
        ''' Start a vm. '''
        vm = VM(key=name)
        print vm.start()

    def stop(self, name):
        ''' Stop a vm. '''
        vm = VM(key=name)
        print vm.stop()

    def destroy(self, name):
        ''' Destroy a vm. '''
        vm = VM(key=name)
        print vm.destroy()

    def delete(self, name):
        ''' Delete a vm. '''
        vm = VM(key=name)
        print vm.delete()

# This has a 'K' because it's more raw that way...
# It will be renamed back to the 'correct' spelling once this tool isn't
# directly hitting everything and is actually using the rpc interface.
class Konfig(Command):
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
    'config': Konfig,
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

def display_help(msg, kls, ret=1):
    ''' Print help message '''
    print >> sys.stderr, msg
    kls.help()
    sys.exit(ret)

def main(argv):
    ''' Program entry point '''
    if len(argv) < 1:
        display_help("Missing Command", Help)

    cmd = argv.pop(0)

    if cmd == 'display_help':
        display_help("Help", Help, 0)

    try:
        command = COMMAND_MAP[cmd]()
    except KeyError:
        if DEBUG:
            traceback.print_exc(file=sys.stderr)
        display_help("Unknown Command", Help)

    try:
        sub = argv.pop(0)
    except IndexError:
        if DEBUG:
            traceback.print_exc(file=sys.stderr)
        display_help("Missing Action", command)

    try:
        func = getattr(command, sub)
    except AttributeError:
        if DEBUG:
            traceback.print_exc(file=sys.stderr)
        display_help("Unknown Action", Help)

    count = len(argv)
    amin, amax = arg_count(func)
    if amin <= count <= amax:
        try:
            func(*argv)
        except KeyboardInterrupt:
            sys.exit()
        except Exception:
            print >> sys.stderr, "Error running command:"
            if DEBUG:
                traceback.print_exc(file=sys.stderr)
            sys.exit(1)
    else:
        msg = "Not enough" if count < amin else "Too many"
        msg +=" Arguments"
        display_help(msg, command)

if __name__ == '__main__':
    main(sys.argv[1:])


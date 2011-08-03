import traceback
from omg.log import hoses
from omg.log.levels import LEVEL_STR

class FileLog():
    def __init__(self, service=None, path=None):
        if not service:
            service = 'generic'
        if not path:
            path = '/var/log/omg'
        self.path = '%s/omg-%s.log' % (path, service)
        self.open()

    def write(self, data):
        self.fp.write(data)
        self.fp.flush()

    def open(self):
        self.fp = open(self.path, 'a+')

    def drip(self, msg, level):
        self.write("%s: %s\n" % (LEVEL_STR[level], msg))

    def open_files(self):
        return [self.fp]

hoses['file'] = FileLog

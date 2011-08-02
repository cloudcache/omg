from omg.log import Log

class FileLog():
    def __init__(self, path=None):
        if not path:
            path = '/var/log/omg/omg.log'
        self.path = path
        self.fp = None

    def write(self, data):
        if not self.fp:
            self.open()
        self.fp.write(data)
        self.fp.flush()

    def debug(self, msg):
        self.write("DEBUG: %s\n" % msg)

    def open(self):
        self.fp = open(self.path, 'a+')

Log.register(Log, 'file', FileLog)


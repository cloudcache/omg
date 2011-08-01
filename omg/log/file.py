from omg.log import Log

class FileLog(Log):
    def __init__(self, path):
        if not self._state():
            self.path = path
            self.fp = open(path)
            super(FileLog, self).__init__()

    def debug(self, msg):
        self.fp.write("DEBUG: %s\n" % msg)


Log.register(Log, 'file', FileLog)


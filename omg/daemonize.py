import daemon as _daemon
import lockfile
import signal

class Daemon(_daemon.DaemonContext):
    def __init__(self, path, pid):
        super(Daemon, self).__init__(working_directory=path,
            pidfile=lockfile.FileLock(pid))

    def signals(self, smap):
        self.signal_map = smap
    


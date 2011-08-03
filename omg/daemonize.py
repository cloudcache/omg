import daemon as _daemon
import lockfile
import signal
import os

from omg.log.api import open_files, debug

class Daemon(_daemon.DaemonContext):
    def __init__(self, path, pid):
        self.lock = lockfile.FileLock(pid)
        super(Daemon, self).__init__(working_directory=path)
        self.signal_map = {}
  
    def signal(self, sig, handler):
        self.signal_map[sig] = handler

    def check_pid(self):
        try:
            self.lock.acquire(timeout=0)
        except lockfile.AlreadyLocked:
            debug("Unable to lock pid file.")
            return False
        return True

    def update_pid(self):
        with open(self.lock.path+'.lock', 'w') as f:
            f.write(str(os.getpid()))

    def __enter__(self):
        debug("Entering daemon Context")
        self.files_preserve = open_files()
        super(Daemon, self).__enter__()

    def __exit__(self, t, v, tb):
        debug("Exiting daemon Context")
        self.lock.release()
        super(Daemon, self).__exit__(t, v, tb)


